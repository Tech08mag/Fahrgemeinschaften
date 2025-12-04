# Fahrgemeinschaften

A carpooling/rideshare web application with a German language interface.

## Overview

This is a web application for coordinating carpools (Fahrgemeinschaften in German). The project consists of:
- **Backend**: Python Flask server serving static files
- **Frontend**: Static HTML pages with Tailwind CSS for styling
- **Language**: German (Deutschland)

## Project Structure

```
.
├── frontend/           # Frontend HTML pages
│   ├── index.html     # Main landing page (currently empty)
│   ├── login.html     # Login page with Tailwind CSS
│   ├── register.html  # Registration page
│   └── settings.html  # Settings page (currently minimal)
├── main.py            # Flask web server
├── pyproject.toml     # Python project configuration
└── uv.lock            # UV package lock file
```

## Tech Stack

- **Python**: 3.13
- **Web Framework**: Flask 3.1.2
- **Package Manager**: UV
- **CSS Framework**: Tailwind CSS (via CDN)
- **Server**: Flask development server (bound to 0.0.0.0:5000)

## Recent Changes

**December 4, 2025** - Initial Replit Setup
- Installed Python 3.13
- Added Flask as dependency
- Created Flask web server to serve static HTML files
- Configured workflow to run on port 5000
- Set up deployment configuration for autoscale deployment
- Server configured to bind to 0.0.0.0:5000 for Replit environment

## Development

The Flask server is configured to:
- Serve static files from the `frontend/` directory
- Bind to `0.0.0.0:5000` to work with Replit's proxy
- Handle routing for all HTML pages

### Running Locally

The application runs automatically via the "Flask Server" workflow. To run manually:

```bash
python main.py
```

The server will start on http://0.0.0.0:5000

## Deployment

The project is configured for **autoscale** deployment, which is suitable for this stateless web application. The deployment will automatically start the Flask server.

## Frontend Pages

- `/` - Main index page (empty template)
- `/login.html` - Login page with username/password form
- `/register.html` - Registration page with username and password confirmation
- `/settings.html` - Settings page (minimal template)

All pages use Tailwind CSS via CDN for styling and follow a consistent dark theme design.

## Dependencies

Python packages (managed by UV):
- flask==3.1.2
- werkzeug==3.1.4
- jinja2==3.1.6
- click==8.3.1
- blinker==1.9.0
- itsdangerous==2.2.0
- markupsafe==3.0.3

## Notes

- The application currently serves static HTML pages
- No backend authentication or database functionality is implemented yet
- Forms on login/register pages have no submit handlers yet
- The project is ready for further development of backend functionality
