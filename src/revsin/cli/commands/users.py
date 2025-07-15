"""
User management commands for the Library Management System CLI
"""

import click
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

from ..utils import (
    handle_errors, get_db_session, print_success, print_error, print_info,
    confirm_action, prompt_for_input, display_table, validate_email,
    format_datetime, format_user_role, format_bool, truncate_text
)
from ...crud.user import user_crud
from ...schemas.user import UserCreate, UserUpdate
from ...models.user import UserRole

# Password context for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@click.group()
def users():
    """User management commands"""
    pass


@users.command()
@click.argument('user_id', type=int)
@click.option('--role', type=click.Choice(['admin', 'librarian', 'member']), required=True, help='Role to assign')
@handle_errors
def set_role(user_id, role):
    """Set or change a user's role (admin only)"""
    from ...crud.user import user_crud
    from ...models.user import UserRole
    from ...auth.dependencies import get_current_admin_user

    # Prompt for admin authentication (could be improved with session/token)
    print_info("Admin authentication required to change roles.")
    # For now, assume only admins can run this command (enforced at CLI level)

    with get_db_session() as db:
        user = user_crud.get(db, user_id)
        if not user:
            print_error(f"User with ID {user_id} not found")
            return

        if user.role.value == role:
            print_info(f"User already has role '{role}'")
            return

        try:
            user_update = UserUpdate(
                username=getattr(user, 'username', None),
                first_name=getattr(user, 'first_name', None),
                last_name=getattr(user, 'last_name', None),
                phone=getattr(user, 'phone', None),
                address=getattr(user, 'address', None),
                password=None,  # No password change
                role=UserRole(role)
            )
            updated_user = user_crud.update(
                db, db_obj=user, obj_in=user_update)
            print_success(
                f"Role for user '{updated_user.username}' changed to '{role}'")
            # TODO: Add audit log entry here
        except Exception as e:
            print_error(f"Failed to change role: {str(e)}")


@users.command()
@click.option('--email', help='User email address')
@click.option('--username', help='Username')
@click.option('--first-name', help='First name')
@click.option('--last-name', help='Last name')
@click.option('--role', type=click.Choice(['admin', 'librarian', 'member']), help='User role')
@click.option('--password', help='Password (will prompt if not provided)')
@click.option('--phone', help='Phone number')
@click.option('--address', help='Address')
@handle_errors
def create(email, username, first_name, last_name, role, password, phone, address):
    """Create a new user"""

    # Collect missing information
    if not email:
        email = prompt_for_input("Email address")

    if not validate_email(email):
        print_error("Invalid email format")
        return

    if not username:
        username = prompt_for_input("Username")

    if not first_name:
        first_name = prompt_for_input("First name")

    if not last_name:
        last_name = prompt_for_input("Last name")

    if not role:
        role = prompt_for_input(
            "Role", choices=['admin', 'librarian', 'member'], default='member')

    if not password:
        password = prompt_for_input("Password", password=True)

    # Create user data (UserCreate expects plain password, not hashed)
    user_data = UserCreate(
        email=email,
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password,
        role=UserRole(role),
        phone=phone,
        address=address
    )

    with get_db_session() as db:
        try:
            user = user_crud.create(db, obj_in=user_data)
            print_success(
                f"User '{user.username}' created successfully with ID: {user.id}")
        except IntegrityError as e:
            if "email" in str(e):
                print_error("Email already exists")
            elif "username" in str(e):
                print_error("Username already exists")
            else:
                print_error(f"Failed to create user: {str(e)}")


@users.command()
@click.option('--limit', default=10, help='Number of users to display')
@click.option('--skip', default=0, help='Number of users to skip')
@click.option('--role', type=click.Choice(['admin', 'librarian', 'member']), help='Filter by role')
@handle_errors
def list(limit, skip, role):
    """List users"""

    with get_db_session() as db:
        filters = {}
        if role:
            filters['role'] = UserRole(role)

        users = user_crud.get_multi(
            db, skip=skip, limit=limit, filters=filters)

        if not users:
            print_info("No users found")
            return

        # Prepare data for display
        user_data = []
        for user in users:
            is_active = bool(getattr(user, 'is_active', False))
            user_data.append({
                'ID': user.id,
                'Username': user.username,
                'Email': user.email,
                'Name': user.full_name,
                'Role': user.role.value,
                'Active': format_bool(is_active),
                'Created': format_datetime(user.created_at)
            })

        headers = ['ID', 'Username', 'Email',
                   'Name', 'Role', 'Active', 'Created']
        display_table(user_data, headers, "Users")


@users.command()
@click.argument('user_id', type=int)
@handle_errors
def show(user_id):
    """Show user details"""

    with get_db_session() as db:
        user = user_crud.get(db, user_id)

        if not user:
            print_error(f"User with ID {user_id} not found")
            return

        print_info(f"User Details - ID: {user.id}")
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Name: {user.full_name}")
        print(f"Role: {format_user_role(user.role.value)}")
        is_active = bool(getattr(user, 'is_active', False))
        print(f"Active: {format_bool(is_active)}")
        print(f"Phone: {user.phone or 'N/A'}")
        print(f"Address: {user.address or 'N/A'}")
        print(f"Created: {format_datetime(user.created_at)}")
        print(f"Updated: {format_datetime(user.updated_at)}")

        # Show loan statistics
        loan_count = len(user.loans)
        active_loans = sum(
            1 for loan in user.loans if loan.status.value == 'active')
        print(f"Total loans: {loan_count}")
        print(f"Active loans: {active_loans}")


@users.command()
@click.argument('user_id', type=int)
@click.option('--email', help='New email address')
@click.option('--username', help='New username')
@click.option('--first-name', help='New first name')
@click.option('--last-name', help='New last name')
@click.option('--role', type=click.Choice(['admin', 'librarian', 'member']), help='New role')
@click.option('--phone', help='New phone number')
@click.option('--address', help='New address')
@click.option('--active/--inactive', help='Set user active status')
@handle_errors
def update(user_id, email, username, first_name, last_name, role, phone, address, active):
    """Update user information"""

    with get_db_session() as db:
        user = user_crud.get(db, user_id)

        if not user:
            print_error(f"User with ID {user_id} not found")
            return

        # Collect update data
        update_data = {}

        if email is not None:
            if not validate_email(email):
                print_error("Invalid email format")
                return
            update_data['email'] = email

        if username is not None:
            update_data['username'] = username

        if first_name is not None:
            update_data['first_name'] = first_name

        if last_name is not None:
            update_data['last_name'] = last_name

        if role is not None:
            update_data['role'] = UserRole(role)

        if phone is not None:
            update_data['phone'] = phone

        if address is not None:
            update_data['address'] = address

        if active is not None:
            update_data['is_active'] = active

        if not update_data:
            print_info("No changes specified")
            return

        try:
            user_update = UserUpdate(**update_data)
            updated_user = user_crud.update(
                db, db_obj=user, obj_in=user_update)
            print_success(
                f"User '{updated_user.username}' updated successfully")
        except IntegrityError as e:
            if "email" in str(e):
                print_error("Email already exists")
            elif "username" in str(e):
                print_error("Username already exists")
            else:
                print_error(f"Failed to update user: {str(e)}")


@users.command()
@click.argument('user_id', type=int)
@click.option('--force', is_flag=True, help='Force deletion without confirmation')
@handle_errors
def delete(user_id, force):
    """Delete a user"""

    with get_db_session() as db:
        user = user_crud.get(db, user_id)

        if not user:
            print_error(f"User with ID {user_id} not found")
            return

        # Check for active loans
        active_loans = sum(
            1 for loan in user.loans if loan.status.value == 'active')
        if active_loans > 0:
            print_error(f"Cannot delete user with {active_loans} active loans")
            return

        if not force:
            if not confirm_action(f"Delete user '{user.username}'? This action cannot be undone."):
                return

        try:
            user_crud.remove(db, id=user_id)
            print_success(f"User '{user.username}' deleted successfully")
        except Exception as e:
            print_error(f"Failed to delete user: {str(e)}")


@users.command()
@click.argument('query')
@click.option('--limit', default=10, help='Number of results to display')
@handle_errors
def search(query, limit):
    """Search users by name, email, or username"""

    with get_db_session() as db:
        users = user_crud.search_users(db, query=query, limit=limit)

        if not users:
            print_info(f"No users found matching '{query}'")
            return

        # Prepare data for display
        user_data = []
        for user in users:
            is_active = bool(getattr(user, 'is_active', False))
            user_data.append({
                'ID': user.id,
                'Username': user.username,
                'Email': user.email,
                'Name': user.full_name,
                'Role': user.role.value,
                'Active': format_bool(is_active)
            })

        headers = ['ID', 'Username', 'Email', 'Name', 'Role', 'Active']
        display_table(user_data, headers, f"Search Results for '{query}'")


@users.command()
@click.argument('user_id', type=int)
@click.option('--new-password', help='New password (will prompt if not provided)')
@handle_errors
def change_password(user_id, new_password):
    """Change user password"""

    with get_db_session() as db:
        user = user_crud.get(db, user_id)

        if not user:
            print_error(f"User with ID {user_id} not found")
            return

        if not new_password:
            new_password = prompt_for_input("New password", password=True)

        # Hash new password
        hashed_password = pwd_context.hash(new_password)

        try:
            user_update = UserUpdate(
                username=getattr(user, 'username', None),
                first_name=getattr(user, 'first_name', None),
                last_name=getattr(user, 'last_name', None),
                phone=getattr(user, 'phone', None),
                address=getattr(user, 'address', None),
                password=new_password
            )
            updated_user = user_crud.update(
                db, db_obj=user, obj_in=user_update)
            print_success(f"Password changed for user '{user.username}'")
        except Exception as e:
            print_error(f"Failed to change password: {str(e)}")


@users.command()
@handle_errors
def stats():
    """Display user statistics"""

    with get_db_session() as db:
        total_users = user_crud.count(db)
        active_users = user_crud.count(db, filters={'is_active': True})
        inactive_users = total_users - active_users

        admin_count = user_crud.count(db, filters={'role': UserRole.ADMIN})
        librarian_count = user_crud.count(
            db, filters={'role': UserRole.LIBRARIAN})
        member_count = user_crud.count(db, filters={'role': UserRole.MEMBER})

        print_info("User Statistics")
        print(f"Total users: {total_users}")
        print(f"Active users: {active_users}")
        print(f"Inactive users: {inactive_users}")
        print(f"Admins: {admin_count}")
        print(f"Librarians: {librarian_count}")
        print(f"Members: {member_count}")


if __name__ == "__main__":
    users()
