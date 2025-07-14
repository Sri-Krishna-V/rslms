# RevSin Documentation 📚

Welcome to the comprehensive documentation for the **RevSin Library Management System** - a modern, feature-rich solution for libraries of all sizes.

## 🌟 What's Included

This documentation covers every aspect of RevSin, from quick setup to advanced deployment:

### 📖 **Complete User Guide**
- **Getting Started**: Installation and initial setup
- **CLI Mastery**: Interactive, colorful command-line interface  
- **API Reference**: Complete REST API with examples
- **User Management**: Roles, permissions, and workflows
- **Book Management**: Catalog, search, and inventory
- **Loan Management**: Borrowing, returns, and fines

### 🛠 **Developer Resources**
- **Architecture Overview**: System design and components
- **API Documentation**: Detailed endpoint specifications
- **Database Models**: Complete schema reference
- **Authentication**: JWT and role-based security
- **Development Setup**: Contributing and testing
- **Deployment Guides**: Production deployment options

### 🎨 **Rich CLI Documentation**
RevSin features a **beautiful, interactive CLI** with:
- 🌈 Rich color coding and emojis
- 📊 Interactive tables and progress bars
- 🤖 Smart prompts with validation
- ✅ Confirmation dialogs for safety
- 🎉 Success animations and celebrations

## 📁 Documentation Structure

```
docs/
├── README.md                 # This overview
├── build_docs.py            # Documentation build script
├── sphinx/                  # Sphinx documentation source
│   ├── index.rst           # Main documentation index
│   ├── introduction.rst     # System overview
│   ├── installation.rst     # Setup and installation
│   ├── api/                # API documentation
│   │   ├── index.rst       # API overview
│   │   ├── auth.rst        # Authentication endpoints
│   │   ├── users.rst       # User management API
│   │   ├── books.rst       # Book management API
│   │   └── loans.rst       # Loan management API
│   ├── cli/                # CLI documentation
│   │   ├── index.rst       # CLI overview
│   │   ├── system.rst      # System commands
│   │   ├── users.rst       # User commands  
│   │   ├── books.rst       # Book commands
│   │   └── loans.rst       # Loan commands
│   ├── models/             # Database models
│   ├── auth/               # Authentication system
│   ├── crud/               # CRUD operations
│   ├── deployment/         # Production deployment
│   ├── development/        # Development guides
│   └── user_guide/         # End-user guides
└── user_guide/             # Additional user documentation
```

## 🚀 Building the Documentation

### Prerequisites
```bash
# Install documentation dependencies
uv sync -G docs
# or
pip install -e ".[docs]"
```

### Build Commands

**Option 1: Using the Build Script (Recommended)**
```bash
# Build and serve documentation
python docs/build_docs.py

# Build only (no serving)
python docs/build_docs.py --no-serve

# Clean build
python docs/build_docs.py --clean
```

**Option 2: Using Sphinx Directly**
```bash
cd docs/sphinx
make html                    # Build HTML documentation
make clean                   # Clean build artifacts
make livehtml               # Build with auto-reload
```

**Option 3: Using UV**
```bash
# Build with UV task runner
uv run docs:build           # Build documentation
uv run docs:serve           # Build and serve
uv run docs:clean           # Clean build
```

### Viewing Documentation

After building, open one of these URLs:
- **Local Build**: `docs/sphinx/_build/html/index.html`
- **Live Server**: `http://localhost:8000` (when using `--serve`)

## 📝 Documentation Standards

### Writing Guidelines

**Style & Tone**
- Write in clear, concise language
- Use active voice when possible
- Include practical examples for complex concepts
- Maintain a friendly, helpful tone

**Formatting Standards**
- Use **Markdown** for simple documentation files
- Use **reStructuredText** for Sphinx documentation
- Include code examples with proper syntax highlighting
- Use emojis sparingly but effectively for visual appeal

**Code Examples**
- Test all code examples to ensure they work
- Include complete, runnable examples when possible
- Show both successful and error scenarios
- Use realistic data in examples

### Content Organization

**Structure Requirements**
- Start each section with a clear overview
- Include practical examples early
- Progress from basic to advanced concepts
- End with troubleshooting or next steps

**Cross-References**
- Link to related sections using `:doc:` directives
- Reference API endpoints and CLI commands consistently
- Provide navigation breadcrumbs for complex topics

## 🔧 Advanced Features

### Extensions Used

The documentation uses several Sphinx extensions:

```python
extensions = [
    "sphinx.ext.autodoc",      # Auto-generate from docstrings
    "sphinx.ext.viewcode",     # Include source code links
    "sphinx.ext.napoleon",     # Google/NumPy docstring support
    "sphinx.ext.intersphinx",  # Cross-project linking
    "sphinx.ext.autosummary",  # Auto-summary tables
    "sphinx_autodoc_typehints", # Type hint support
]
```

### Theme Customization

- **Theme**: Sphinx RTD Theme with custom styling
- **Colors**: Consistent with RevSin branding
- **Navigation**: Hierarchical with clear sections
- **Search**: Full-text search with filtering

### Interactive Elements

- **Code Blocks**: Syntax highlighting for multiple languages
- **Tables**: Responsive tables with sorting
- **Admonitions**: Notes, warnings, and tips
- **Cross-References**: Automatic linking between sections

## 📋 Contributing to Documentation

### Quick Contribution Guide

1. **Find or Create Issue**: Document what needs updating
2. **Edit Content**: Make changes to `.rst` or `.md` files
3. **Test Build**: Run `python docs/build_docs.py` to verify
4. **Submit PR**: Include screenshots of significant visual changes

### Documentation Checklist

Before submitting documentation changes:

- [ ] Content is accurate and up-to-date
- [ ] Code examples are tested and working
- [ ] Cross-references are correct
- [ ] Build completes without errors or warnings
- [ ] Changes are reflected in table of contents
- [ ] Language is clear and consistent

### Common Tasks

**Adding New Sections**
```bash
# Create new .rst file
touch docs/sphinx/new_section.rst

# Add to appropriate toctree in index.rst
# Build and verify navigation
```

**Updating API Documentation**
```bash
# API docs auto-generate from docstrings
# Update docstrings in source code
# Rebuild documentation to see changes
```

**Adding CLI Examples**
```bash
# Test CLI commands work as expected
# Include both input and output in examples
# Use realistic scenarios
```

## 🎯 Documentation Goals

### Primary Objectives

1. **Accessibility**: Easy for new users to get started
2. **Completeness**: Cover all features comprehensively  
3. **Accuracy**: Keep synchronized with code changes
4. **Usability**: Intuitive navigation and search
5. **Visual Appeal**: Rich formatting and clear examples

### Success Metrics

- **User Feedback**: Positive community response
- **Adoption**: Increased usage of documented features
- **Maintenance**: Easy to keep updated
- **Search**: Users can find answers quickly
- **Completeness**: No major gaps in coverage

## 🛠 Maintenance

### Regular Tasks

- **Monthly**: Review and update version numbers
- **Per Release**: Update changelog and feature docs  
- **Quarterly**: Review structure and organization
- **As Needed**: Fix broken links and outdated examples

### Automated Checks

The documentation includes automated validation:
- **Link Checking**: Verify all internal and external links
- **Code Testing**: Validate code examples in CI/CD
- **Build Verification**: Ensure clean builds on all platforms
- **Style Consistency**: Automated formatting and linting

## 🚀 Deployment

### GitHub Pages (Recommended)

Documentation automatically deploys to GitHub Pages on:
- Pushes to `main` branch
- New releases/tags
- Manual workflow triggers

### Local Development Server

For real-time editing and preview:
```bash
# Start live-reload server
make livehtml

# Or use the build script
python docs/build_docs.py --live
```

### Production Hosting

For custom domain hosting:
1. Build static HTML: `make html`
2. Deploy `_build/html/` directory
3. Configure web server (Apache, Nginx, etc.)
4. Set up SSL certificate

---

## 📞 Documentation Support

**Need Help?**
- 📖 Check existing documentation first
- 🐛 Open issue for missing/incorrect docs
- 💬 Join discussions for questions
- 🚀 Submit PR for improvements

**Quick Links:**
- [Main Documentation](sphinx/_build/html/index.html)
- [API Reference](sphinx/_build/html/api/index.html)  
- [CLI Guide](sphinx/_build/html/cli/index.html)
- [Installation Guide](sphinx/_build/html/installation.html)

---

*Documentation last updated: November 2024*
*RevSin Version: 0.1.0* 