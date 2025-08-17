# Student Management System

## Overview

A Flask-based web application for managing student records, course catalogs, enrollments, and grades. The system provides a comprehensive dashboard for educational institutions to track student performance, manage course offerings, and maintain academic records. Built with Flask, Bootstrap, and in-memory data storage for simplicity and rapid development.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templating with Flask for server-side rendering
- **UI Framework**: Bootstrap 5 with dark theme for responsive design
- **Icons**: Font Awesome for consistent iconography
- **JavaScript**: Vanilla JavaScript for form validation, tooltips, and interactive features
- **Styling**: Custom CSS for grade badges, avatar circles, and application-specific styling

### Backend Architecture
- **Web Framework**: Flask with modular route organization
- **Application Structure**: 
  - `app.py`: Application factory and configuration
  - `routes.py`: All HTTP route handlers and business logic
  - `models.py`: Data models with CRUD operations
  - `main.py`: Application entry point
- **Session Management**: Flask sessions with configurable secret key
- **Proxy Support**: ProxyFix middleware for deployment behind reverse proxies

### Data Storage
- **Storage Type**: In-memory data storage using Python dictionaries
- **Data Models**: Four main entities - Students, Courses, Enrollments, and Grades
- **Data Persistence**: Singleton DataStore class managing all application data
- **ID Management**: Auto-incrementing integer IDs for all entities
- **Relationships**: Manual relationship management through foreign key references

### Key Features
- **Student Management**: CRUD operations with search functionality and GPA calculation
- **Course Catalog**: Course creation with credit hours and enrollment tracking
- **Enrollment System**: Student-course enrollment with validation
- **Grade Management**: Letter grade assignment with GPA calculation
- **Dashboard**: Summary statistics and navigation hub
- **Reports**: Analytics and performance tracking views

### Design Patterns
- **MVC Pattern**: Clear separation between models, views (templates), and controllers (routes)
- **Factory Pattern**: Application creation with configuration
- **Singleton Pattern**: Global data store instance
- **Template Inheritance**: Base template with consistent navigation and styling

## External Dependencies

### Frontend Dependencies
- **Bootstrap 5**: CSS framework loaded from Replit CDN with dark theme
- **Font Awesome 6.4.0**: Icon library from cdnjs.cloudflare.com
- **Custom Stylesheets**: Local CSS for application-specific styling

### Backend Dependencies
- **Flask**: Core web framework
- **Werkzeug**: WSGI utilities including ProxyFix middleware

### Development Tools
- **Python Standard Library**: datetime, json, typing, os, logging
- **No Database**: Uses in-memory storage instead of external database
- **No Authentication**: Simple session-based state management without user authentication
- **No External APIs**: Self-contained application without third-party service integrations