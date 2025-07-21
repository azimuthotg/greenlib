# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django web application called "Green Library" (NPU Green Library) - an environmental sustainability documentation and reporting system for Nakhon Phanom University. The system manages environmental evidence, blog posts, and infographic data.

## Development Commands

### Running the Application
```bash
python manage.py runserver
```

### Database Operations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Static Files
```bash
# Collect static files
python manage.py collectstatic
```

## Application Architecture

### Django Apps Structure
The project consists of several Django apps:

1. **greenweb** - Main app for environmental data management
   - Models: Year, Category, Issue, Indicator, Evidence
   - Handles hierarchical evidence documentation

2. **docChecker** - Document verification system
   - Models: Year, CategoryGroup, Category, Issue, Indicator, Evidence  
   - More complex hierarchy with category groups
   - User tracking and file management

3. **blogs** - Information/blog management
   - Model: Information with image galleries
   - Handles events, projects, and training content
   - Custom image upload naming with date-based organization

4. **info_graph** - Data visualization
   - Models: Year, Month, DataEntry
   - Environmental metrics tracking (greenhouse gas, electricity, etc.)

5. **category** - Basic category management
   - Simple category structure

6. **indexweb** - Homepage/landing page

### Key Features

- **Hierarchical Evidence Management**: Year → Category(Group) → Issue → Indicator → Evidence
- **File Management**: Multiple upload directories (attachments/, evidence/, imageBlogs/)
- **Multi-language**: Thai language interface with Buddhist calendar support
- **Admin Interface**: Custom reordering with admin_reorder package
- **Static Files**: Organized CSS/JS/images in static/frontend/

### Database Configuration

- Uses MySQL database (greenlibrary)
- Production: Remote server at 202.29.55.213
- Development: Commented local configuration available
- Uses utf8mb4 charset for Thai language support

### Important Technical Notes

- **Thai Date Conversion**: Built-in function converts Gregorian to Buddhist calendar
- **Custom File Naming**: Evidence files use slugified names, blog images use date-based naming
- **Model Relationships**: Extensive use of ForeignKey relationships for hierarchical data
- **Django 5.0.6**: Recent Django version with modern features

### File Upload Patterns

- Evidence files: `evidence/` directory with slugified names
- Blog images: `imageBlogs/YYYY-MM-DD-count-index.ext` format
- General attachments: `attachments/` directory

### URL Structure

- `/admin/` - Django admin interface
- `/web/` - Main greenweb application
- `/info_graph/` - Data visualization
- `/` - Homepage (indexweb)

### Dependencies

- Django==5.0.6
- MySQL database backend
- admin_reorder for custom admin interface
- django_filters for filtering
- Static files management for frontend assets