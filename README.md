# Rfam Web (Django)

A modern Django-based rewrite of the Rfam website, replacing the legacy Perl/Catalyst implementation.

## Overview

This repository contains:

- **rfam-webcode/** - The new Django web application with REST API
- **tests/** - Comprehensive test suite (108 tests) for validating the implementation

## Quick Start

### Running the Django Application

```bash
cd rfam-webcode

# Create virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Build frontend assets (first time only)
npm install
npm run build

# Run the development server
python manage.py runserver 8888
```

The API will be available at http://localhost:8888

### Frontend Development

The project uses the [Visual Framework](https://stable.visual-framework.dev/) (VF) for styling, consistent with EMBL-EBI websites.

```bash
cd rfam-webcode

# Install Node.js dependencies
npm install

# Build CSS (compile SCSS to CSS)
npm run build

# Watch for changes during development
npm run watch
```

**Frontend Structure:**
- `src/scss/main.scss` - Custom Rfam SCSS styles
- `api/static/css/` - Compiled CSS output
- `templates/base.html` - Base template with VF components
- VF Core CSS is loaded from CDN for performance

**Test Visual Framework:**
Visit http://localhost:8888/vf-test to verify VF components are rendering correctly.

### Running Tests

```bash
cd tests

# Create virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure to test against local Django server
# Edit config.yaml: base_url: "http://localhost:8888"

# Run all tests
pytest -v

# Run fast tests only
pytest -m "not slow" -v
```

## Repository Structure

```
rfam-webcode/
├── rfam-webcode/               # Django application
│   ├── api/                    # Main API app
│   │   ├── models.py           # Database models (Rfam MySQL)
│   │   ├── views.py            # API views and endpoints
│   │   ├── serializers.py      # DRF serializers
│   │   ├── forms.py            # Django forms
│   │   ├── urls.py             # URL routing
│   │   ├── static/css/         # Compiled CSS assets
│   │   └── templates/          # App-specific templates
│   ├── rfam_web/               # Django project settings
│   │   ├── settings.py         # Configuration
│   │   └── urls.py             # Root URL config
│   ├── templates/              # Project-level templates
│   │   ├── base.html           # Base template (VF components)
│   │   └── vf_test.html        # VF test page
│   ├── src/scss/               # SCSS source files
│   │   └── main.scss           # Custom Rfam styles
│   ├── package.json            # Node.js dependencies
│   ├── gulpfile.js             # Gulp build configuration
│   ├── manage.py               # Django management script
│   └── requirements.txt        # Python dependencies
│
├── tests/                      # Test suite
│   ├── test_*.py               # Test files (108 tests)
│   ├── config.yaml             # Test configuration
│   ├── conftest.py             # Pytest fixtures
│   └── requirements.txt        # Test dependencies
│
└── .gitignore
```

## API Endpoints

### Families
| Endpoint | Description |
|----------|-------------|
| `GET /family/{acc}` | Get family by accession or ID (JSON/XML) |
| `GET /family/{acc}/alignment` | Download alignment (multiple formats) |
| `GET /family/{acc}/tree` | Phylogenetic tree data |
| `GET /family/{acc}/cm` | Covariance model |
| `GET /family/{acc}/structures` | 3D structure mappings |
| `GET /families` | List all families |
| `GET /families/{letter}` | Filter families by starting letter |
| `GET /families/top20` | Top 20 largest families |
| `GET /families/with_structure` | Families with 3D structures |

### Clans
| Endpoint | Description |
|----------|-------------|
| `GET /clan/{acc}` | Get clan by accession or ID |
| `GET /clans` | List all clans |

### Genomes
| Endpoint | Description |
|----------|-------------|
| `GET /genome/{ncbi_id}` | Get genome by NCBI taxonomy ID |
| `GET /genomes` | List all genomes |
| `GET /genomes/{kingdom}` | Filter by kingdom |

### Motifs
| Endpoint | Description |
|----------|-------------|
| `GET /motif/{acc}` | Get motif by accession or ID |
| `GET /motifs` | List all motifs |

### Search
| Endpoint | Description |
|----------|-------------|
| `GET /search/keyword?query=` | Keyword search |
| `GET /search/taxonomy?query=` | Taxonomy search |
| `GET /search/type?query=` | RNA type search |
| `GET /jump?entry=` | Smart redirect to entity page |

### Forms
| Endpoint | Description |
|----------|-------------|
| `GET/POST /submit_alignment` | Submit Stockholm alignment |

### Other
| Endpoint | Description |
|----------|-------------|
| `GET /` | Home page / API info |
| `GET /status` | Health check |
| `GET /help` | API help |

## Content Negotiation

The API supports multiple output formats via Accept header or query parameter:

```bash
# JSON (default)
curl http://localhost:8888/family/RF00001

# JSON explicit
curl -H "Accept: application/json" http://localhost:8888/family/RF00001

# XML
curl -H "Accept: text/xml" http://localhost:8888/family/RF00001

# Using query parameter
curl "http://localhost:8888/family/RF00001?output=xml"
```

## Configuration

### Database

The application connects to the public Rfam MySQL database by default. Configure via environment variables:

```bash
export RFAM_DB_HOST=mysql-rfam-public.ebi.ac.uk
export RFAM_DB_PORT=4497
export RFAM_DB_NAME=Rfam
export RFAM_DB_USER=rfamro
export RFAM_DB_PASSWORD=
```

### Email (for alignment submissions)

```bash
export EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
export EMAIL_HOST=smtp.example.com
export ALIGNMENT_SUBMISSION_EMAIL=rfam-help@ebi.ac.uk
```

## Test Suite

The test suite validates that the Django implementation matches the behavior of the original Perl/Catalyst site.

### Test Categories

| Category | Tests | Description |
|----------|-------|-------------|
| API | 32 | JSON/XML API responses |
| UI | 58 | HTML page content |
| Search | 12 | Search functionality |
| Integration | 6 | End-to-end workflows |

### Running Specific Tests

```bash
cd tests

# By category
pytest -m api -v          # API tests
pytest -m ui -v           # UI tests
pytest -m search -v       # Search tests

# By file
pytest test_family.py -v
pytest test_static_pages.py::TestSubmitAlignment -v

# Single test
pytest test_family.py::TestFamilyPages::test_family_page_by_accession -v
```

### Test Configuration

Edit `tests/config.yaml` to switch between testing environments:

```yaml
# Test against production
base_url: "https://rfam.org"

# Test against local Django
base_url: "http://localhost:8888"
```

## Development Workflow

1. **Start Django server**: `python manage.py runserver 8888`
2. **Run tests**: `cd tests && pytest -v`
3. **Fix failing tests**: Implement missing functionality
4. **Repeat** until all tests pass

## Dependencies

### Django Application
- Django 5.0+
- Django REST Framework
- PyMySQL
- python-dotenv

### Frontend (Node.js)
- Node.js 18+
- Gulp 5.x (SCSS compilation)
- Sass (SCSS compiler)
- Visual Framework components (loaded from CDN + npm)

### Test Suite
- pytest
- requests
- beautifulsoup4
- lxml
- pytest-html

## Resources

- **Rfam Website**: https://rfam.org
- **Rfam Documentation**: https://docs.rfam.org
- **Rfam Database**: https://ftp.ebi.ac.uk/pub/databases/Rfam

## License

This project follows the same license as the Rfam project.

## Support

- **Issues**: GitHub Issues
- **Email**: rfam-help@ebi.ac.uk
