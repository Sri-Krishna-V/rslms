#!/usr/bin/env python
"""
Build the Sphinx documentation for RevSin.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
SPHINX_DIR = DOCS_DIR / "sphinx"
BUILD_DIR = SPHINX_DIR / "_build"


def setup_directories():
    """Create necessary directories if they don't exist."""
    # Create _static and _templates directories if they don't exist
    (SPHINX_DIR / "_static").mkdir(exist_ok=True)
    (SPHINX_DIR / "_templates").mkdir(exist_ok=True)


def clean_build_dir():
    """Clean the build directory."""
    if BUILD_DIR.exists():
        print(f"Cleaning build directory: {BUILD_DIR}")
        shutil.rmtree(BUILD_DIR)


def build_html():
    """Build the HTML documentation."""
    print("Building HTML documentation...")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "sphinx.cmd.build",
            "-b",
            "html",
            SPHINX_DIR,
            BUILD_DIR / "html",
        ],
        check=False,
    )

    if result.returncode != 0:
        print("Error building HTML documentation")
        return False

    print(f"HTML documentation built successfully: {BUILD_DIR / 'html'}")
    return True


def build_pdf():
    """Build the PDF documentation using LaTeX."""
    print("Building PDF documentation...")

    # First, build the LaTeX files
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "sphinx.cmd.build",
            "-b",
            "latex",
            SPHINX_DIR,
            BUILD_DIR / "latex",
        ],
        check=False,
    )

    if result.returncode != 0:
        print("Error building LaTeX documentation")
        return False

    # Check if pdflatex is available
    if shutil.which("pdflatex") is None:
        print("pdflatex not found, skipping PDF generation")
        return False

    # Build the PDF from the LaTeX files
    os.chdir(BUILD_DIR / "latex")
    result = subprocess.run(["make"], check=False)

    if result.returncode != 0:
        print("Error building PDF from LaTeX files")
        return False

    # Copy the PDF to the html directory
    pdf_file = next(BUILD_DIR.glob("latex/*.pdf"), None)
    if pdf_file:
        shutil.copy(pdf_file, BUILD_DIR / "html")
        print(f"PDF documentation built successfully: {pdf_file}")
        return True

    print("No PDF file found")
    return False


def main():
    """Main function to build the documentation."""
    # Set up directories
    setup_directories()

    # Clean build directory
    clean_build_dir()

    # Build HTML documentation
    html_success = build_html()

    # Build PDF documentation
    pdf_success = build_pdf()

    # Print summary
    print("\nBuild Summary:")
    print(f"HTML: {'Success' if html_success else 'Failed'}")
    print(f"PDF: {'Success' if pdf_success else 'Failed or Skipped'}")

    if html_success:
        print(
            f"\nDocumentation available at: {BUILD_DIR / 'html' / 'index.html'}")


if __name__ == "__main__":
    main()
