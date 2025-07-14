# 📚 RevSin Library Management System

> **A simple, powerful library management system that makes managing books, users, and loans a breeze!**

[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue?style=flat-square&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

---

## 🤔 What is RevSin?

**RevSin** is a modern library management system that helps librarians and library staff efficiently manage:

- **📖 Books**: Add, search, and organize your book collection
- **👥 Users**: Manage library members and staff accounts  
- **📑 Loans**: Track who borrowed what and when it's due
- **💰 Fines**: Handle overdue books and fine payments

**Perfect for**: School libraries, public libraries, community centers, or any organization that lends books to people.

### ✨ Why Choose RevSin?

- **🎨 Beautiful Interface**: Colorful, easy-to-use command-line tools
- **🚀 Fast & Reliable**: Built with modern technology for speed
- **🔐 Secure**: Proper user authentication and permissions
- **📱 API Ready**: Integrate with websites or mobile apps
- **💡 Beginner Friendly**: Clear documentation and helpful error messages

---

## 🚀 Quick Start (5 Minutes!)

### Step 1: Check if you have Python
```bash
python --version
# Should show Python 3.12 or higher
```

**Don't have Python?** → [Download it here](https://python.org/downloads)

### Step 2: Get RevSin
```bash
# Download RevSin
git clone <repository-url>
cd revsin

# Install everything you need (this might take a minute)
pip install uv  # Fast package manager
uv sync         # Install RevSin and dependencies
```

### Step 3: Set up your library
```bash
# Copy the example settings
cp env.example .env

# Edit .env with your database info (see "Easy Setup" below)
```

### Step 4: Start your library!
```bash
# Set up the database
python cli.py system init-db

# Create your first librarian account
python cli.py users create

# Start the system
python run.py
```

🎉 **You're done!** Visit http://localhost:8000/docs to see your library system!

---

## 🛠 Easy Setup Options

### Option A: For Beginners (Cloud Setup - Recommended)
**No database installation needed!** Use free cloud services:

1. **Database**: Sign up at [NeonDB](https://neon.tech) (free tier available)
2. **Cache**: Sign up at [Upstash Redis](https://upstash.com) (free tier available)
3. Copy the connection strings to your `.env` file

**Example .env for cloud setup:**
```bash
DATABASE_URL=postgresql://your-neon-db-connection-string
REDIS_URL=redis://your-upstash-redis-string
SECRET_KEY=make-this-a-random-string-123
ENVIRONMENT=development
```

### Option B: For Advanced Users (Local Setup)
If you prefer running everything locally:

1. Install PostgreSQL and Redis on your computer
2. Create a database named "revsin"
3. Update your `.env` file with local connections

---

## 🎨 What Can You Do?

### Command Line Tools (CLI)
RevSin comes with beautiful, colorful command-line tools:

```bash
# Check if everything is working
python cli.py system health

# Add a book to your library
python cli.py books add

# See all your users
python cli.py users list

# Check loan statistics
python cli.py loans stats
```

### Web API
Build websites or mobile apps using our API:

- **Browse books**: `GET /api/v1/books/`
- **Create loans**: `POST /api/v1/loans/`
- **Manage users**: `GET /api/v1/users/`

📖 **Full API Documentation**: http://localhost:8000/docs

### Features Overview

| Feature | What it does | Who can use it |
|---------|-------------|----------------|
| **User Management** | Add librarians, members, admins | Admins |
| **Book Catalog** | Search, add, update books | Librarians, Admins |
| **Loan Tracking** | Check out/in books, renewals | Everyone |
| **Fine Management** | Calculate and track overdue fines | Librarians, Admins |
| **Reports & Stats** | See popular books, overdue items | Librarians, Admins |

---

## 👥 User Types

### 👑 Admin
- **Can do**: Everything! Manage users, books, system settings
- **Perfect for**: Library directors, IT administrators

### 📋 Librarian  
- **Can do**: Manage books and loans, help patrons
- **Perfect for**: Front desk staff, circulation desk workers

### 📖 Member
- **Can do**: Search books, view their loans, pay fines
- **Perfect for**: Library patrons, students, community members

---

## 🆘 Need Help?

### Common Questions

**"I get an error when starting!"**
```bash
# Check system health - this will tell you what's wrong
python cli.py system health

# Or run the doctor for detailed diagnostics
python cli.py system doctor
```

**"How do I add my first books?"**
```bash
# Interactive book addition (asks you questions)
python cli.py books add

# Or add multiple books from a file
python cli.py books import my-books.csv
```

**"Can I reset everything and start over?"**
```bash
# ⚠️ WARNING: This deletes all data!
python cli.py system reset-db
```

### Getting Support
- 📖 **Documentation**: [Full documentation here](docs/sphinx/_build/html/index.html)
- 🐛 **Found a bug?**: [Open an issue](https://github.com/yourusername/revsin/issues)
- 💬 **Questions?**: [Start a discussion](https://github.com/yourusername/revsin/discussions)

---

## 🔧 Advanced Features

<details>
<summary>🖥 Production Deployment</summary>

### Running in Production

For libraries serving many users:

```bash
# Production server with multiple workers
python run_production.py

# Or manually with Gunicorn
uv run gunicorn src.revsin.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

**Production Checklist:**
- ✅ Use strong passwords and secret keys
- ✅ Enable HTTPS
- ✅ Set up database backups
- ✅ Configure monitoring

</details>

<details>
<summary>⚙️ Configuration Options</summary>

### Environment Variables

All settings are controlled through your `.env` file:

| Setting | What it does | Example |
|---------|-------------|---------|
| `DATABASE_URL` | Where your books/users are stored | `postgresql://user:pass@host:port/db` |
| `REDIS_URL` | Cache for faster performance | `redis://host:port` |
| `SECRET_KEY` | Security key (keep this secret!) | `your-random-secret-123` |
| `ENVIRONMENT` | development or production | `development` |
| `DEBUG` | Show detailed error messages | `true` |

</details>

<details>
<summary>🛠 Development & Contributing</summary>

### For Developers

Want to improve RevSin or add features?

```bash
# Set up development environment
uv sync -G dev -G docs -G test

# Run tests
uv run pytest

# Format code
uv run black src/
uv run isort src/

# Check for issues
uv run flake8 src/
uv run mypy src/
```

**Contributing:**
1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

</details>

<details>
<summary>📊 API Reference</summary>

### REST API Endpoints

#### Authentication
- `POST /api/v1/auth/register` — Create new account
- `POST /api/v1/auth/login` — Login and get access token
- `GET /api/v1/auth/me` — Get current user info

#### Books
- `GET /api/v1/books/` — List all books
- `POST /api/v1/books/` — Add new book (librarian+)
- `GET /api/v1/books/{id}` — Get book details
- `GET /api/v1/books/search?q=python` — Search books

#### Users
- `GET /api/v1/users/` — List users (admin only)
- `GET /api/v1/users/{id}` — Get user details
- `PUT /api/v1/users/{id}` — Update user info

#### Loans
- `GET /api/v1/loans/` — List loans (librarian+)
- `POST /api/v1/loans/` — Create new loan
- `PUT /api/v1/loans/{id}/return` — Return book
- `GET /api/v1/loans/overdue` — Get overdue loans

**Interactive API Docs**: http://localhost:8000/docs

</details>

<details>
<summary>📱 CLI Commands Reference</summary>

### System Commands
```bash
python cli.py system health         # Check if everything is working
python cli.py system init-db        # Set up database tables
python cli.py system clear-cache    # Clear cached data
python cli.py system info           # Show system information
```

### User Management
```bash
python cli.py users create          # Add new user (interactive)
python cli.py users list            # Show all users
python cli.py users search "john"   # Find users
python cli.py users stats           # User statistics
```

### Book Management  
```bash
python cli.py books add             # Add book (interactive)
python cli.py books list            # Show all books
python cli.py books search "python" # Search books
python cli.py books available       # Show available books
```

### Loan Management
```bash
python cli.py loans create          # Create new loan
python cli.py loans list            # Show all loans
python cli.py loans overdue         # Show overdue loans
python cli.py loans stats           # Loan statistics
```

**💡 Tip**: Add `--help` to any command for more options!

</details>

---

## 🏗 Technical Details

<details>
<summary>Tech Stack (for the curious)</summary>

**Backend Technologies:**
- **Python 3.12+**: Modern Python for reliability
- **FastAPI**: Fast web framework for APIs
- **PostgreSQL**: Robust database for your data
- **Redis**: Fast caching for better performance
- **SQLAlchemy**: Database toolkit
- **JWT**: Secure user authentication

**Development Tools:**
- **pytest**: Automated testing
- **Black/isort**: Code formatting
- **Sphinx**: Documentation generation
- **Docker**: Containerization support

</details>

---

## 📄 License

MIT License - feel free to use RevSin in your library!

---

## 🙏 Acknowledgments

Built with ❤️ for librarians and book lovers everywhere.

**Special thanks to:**
- The FastAPI community
- Open source contributors
- Librarians who provided feedback

---

<div align="center">
  <strong>Ready to revolutionize your library management?</strong><br>
  <a href="#-quick-start-5-minutes">Get Started Now!</a> • 
  <a href="docs/sphinx/_build/html/index.html">Read the Docs</a> • 
  <a href="https://github.com/yourusername/revsin/issues">Get Help</a>
</div> 