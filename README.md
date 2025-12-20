# Rfam Test-Driven Development (TDD) Suite

Comprehensive test suite for auditing the current Rfam website (https://rfam.org/) to support Test-Driven Development (TDD) for rewriting the website from Perl/Catalyst to Django.

## 📋 Overview

This repository contains:

- **108 automated tests** covering all major Rfam endpoints and functionality
- Tests for HTML pages, JSON/XML APIs, data exports, search, and more
- Documentation of all current website endpoints
- TDD workflow for Django rewrite
- CI/CD integration with GitHub Actions

## 🚀 Quick Start

```bash
cd tests

# Create virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run fast tests
pytest -m "not slow" -v

# Run all tests
pytest -v

# Generate HTML report
pytest --html=report.html --self-contained-html
```

Or use the convenience script:

```bash
cd tests
./run_tests.sh --help
```

## 📁 Repository Structure

```
Rfam-TDD/
├── rfam-website/           # Cloned Perl/Catalyst source code
├── tests/                  # Test suite
│   ├── conftest.py         # Pytest configuration and fixtures
│   ├── config.yaml         # Test configuration and test data
│   ├── requirements.txt    # Python dependencies
│   ├── pytest.ini          # Pytest settings
│   ├── test_*.py           # Test files (108 tests)
│   ├── README.md           # Detailed test documentation
│   ├── QUICKSTART.md       # Quick start guide
│   ├── ENDPOINTS.md        # Complete endpoint reference
│   └── run_tests.sh        # Convenience test runner
└── .github/
    └── workflows/
        └── test.yml        # CI/CD workflow
```

## 🧪 Test Coverage

The test suite covers:

### Core Entities
- ✅ **Family pages** (RF accessions) - 15 endpoints
- ✅ **Clan pages** (CL accessions) - 3 endpoints
- ✅ **Genome pages** (NCBI taxonomy IDs) - 4 endpoints
- ✅ **Motif pages** (RM accessions) - 3 endpoints

### Functionality
- ✅ **Browse** - Families, clans, genomes, motifs (12 endpoints)
- ✅ **Search** - Sequence, keyword, taxonomy, type, jump (7 endpoints)
- ✅ **API Formats** - JSON and XML
- ✅ **Data Exports** - Alignments (6 formats), trees, GFF, CM
- ✅ **Static Pages** - Home, help, COVID-19, viruses, etc.
- ✅ **Integration Tests** - Complete workflows

### Test Statistics
- **Total Tests**: 108
- **Fast Tests**: 96 (excludes slow downloads/large data)
- **API Tests**: 32
- **UI Tests**: 58
- **Search Tests**: 12
- **Integration Tests**: 6

## 📖 Documentation

- **[tests/README.md](tests/README.md)** - Complete test suite documentation
- **[tests/QUICKSTART.md](tests/QUICKSTART.md)** - Get started in 5 minutes
- **[tests/ENDPOINTS.md](tests/ENDPOINTS.md)** - Reference of all 56+ endpoints

## 🔄 TDD Workflow for Django Rewrite

### 1. Establish Baseline

Run tests against the current Perl/Catalyst site:

```bash
cd tests
pytest --html=baseline-report.html --self-contained-html
```

This creates a baseline of expected behavior.

### 2. Point to Django

Edit `tests/config.yaml`:

```yaml
base_url: "http://localhost:8000"  # Your Django dev server
```

### 3. Implement Django Endpoint

Start with high-priority endpoints:
1. `/family/{acc}` - Family pages (JSON, XML, HTML)
2. `/search/*` - Search functionality
3. `/browse/*` - Browse endpoints
4. `/family/{acc}/alignment` - Data exports

### 4. Run Tests Against Django

```bash
cd tests
pytest test_family.py -v  # Test family endpoints
```

### 5. Iterate Until Passing

For each failing test:
1. Review the test to understand expected behavior
2. Check the baseline report for actual responses
3. Fix your Django implementation
4. Rerun: `pytest test_family.py::TestFamilyPages::test_family_page_by_accession -v`
5. Repeat until all tests pass

### 6. Generate Comparison Report

```bash
pytest --html=django-report.html --self-contained-html
```

Compare with baseline to track progress.

## 🏃 Running Tests

### Basic Commands

```bash
# All tests
pytest

# Verbose output
pytest -v

# Fast tests only (exclude slow downloads)
pytest -m "not slow"

# Specific category
pytest -m api        # API tests only
pytest -m ui         # UI tests only
pytest -m search     # Search tests only

# Specific test file
pytest test_family.py

# Specific test
pytest test_family.py::TestFamilyPages::test_family_page_by_accession

# Parallel execution (faster)
pytest -n auto

# Stop on first failure
pytest -x
```

### Using the Script

```bash
cd tests

# Show help
./run_tests.sh --help

# Fast tests only
./run_tests.sh --fast

# With HTML report
./run_tests.sh --report

# Parallel execution
./run_tests.sh --parallel

# API tests with report
./run_tests.sh --api --report
```

## 🎯 Test Organization

Tests are organized by functionality:

- **test_family.py** - Family pages (HTML, JSON, XML, alignments, trees, images)
- **test_clan.py** - Clan pages and structure mappings
- **test_genome.py** - Genome pages, GFF downloads, kingdom browsing
- **test_motif.py** - Motif pages and browsing
- **test_browse.py** - Browse functionality (families, clans, genomes, motifs)
- **test_search.py** - All search types (sequence, keyword, taxonomy, type, jump)
- **test_static_pages.py** - Home, help, special pages (COVID-19, viruses, etc.)
- **test_sequence.py** - Sequence hits and accession lookups
- **test_alignment_formats.py** - Alignment exports in multiple formats
- **test_species_tree.py** - Tree visualizations
- **test_integration.py** - End-to-end workflows

## ⚙️ Configuration

Edit `tests/config.yaml` to:

- Change base URL (for testing against Django)
- Adjust timeouts
- Add/modify test data
- Configure test parameters

Example:

```yaml
base_url: "http://localhost:8000"
timeout: 60
long_timeout: 120

test_data:
  families:
    - acc: "RF00001"
      id: "5S_rRNA"
      description: "5S ribosomal RNA"
```

## 🔍 Key Endpoints Tested

### Family (RF Accessions)
- `/family/{acc}` - HTML, JSON, XML
- `/family/{acc}/alignment` - Stockholm, Pfam, FASTA, Clustal, Phylip, PSI-BLAST
- `/family/{acc}/tree` - Phylogenetic trees
- `/family/{acc}/cm` - Covariance models
- `/family/{acc}/regions` - Seed/full regions
- `/family/{acc}/structures` - PDB mappings
- `/family/{acc}/image` - Secondary structure diagrams

### Browse
- `/families`, `/families/{letter}`, `/families/with_structure`, `/families/top20`
- `/clans`
- `/genomes`, `/genomes/{kingdom}` (Bacteria, Eukaryota, Archaea, Viruses)
- `/motifs`

### Search
- `/search/sequence` - POST sequence search
- `/search/keyword` - Text search
- `/search/taxonomy` - Species search
- `/search/type` - RNA type search
- `/jump` - Smart search/redirect

### Other
- `/clan/{acc}` - Clan pages
- `/genome/{id}` - Genome annotations
- `/motif/{acc}` - Motif pages
- `/sequence/{acc}` - Sequence hits

See [tests/ENDPOINTS.md](tests/ENDPOINTS.md) for complete list.

## 🤖 Continuous Integration

GitHub Actions workflow (`.github/workflows/test.yml`) runs tests:
- On every push and pull request
- Daily at 2 AM UTC (monitors live site)
- Manually via workflow dispatch
- Tests on Python 3.9, 3.10, and 3.11
- Generates HTML reports as artifacts

## 📊 Test Results Interpretation

### ✅ Passing Tests
- Endpoint exists and returns expected status code
- Response contains expected content type
- Data structure matches expectations
- Error handling works correctly

### ❌ Failing Tests
May indicate:
- Endpoint has changed or been removed
- Data structure changed
- Test data (e.g., RF00001) was modified or removed
- Rate limiting or network issues
- Feature deprecation

Failing tests help identify what needs attention in the Django rewrite.

## 🛠️ Development

### Adding New Tests

1. Identify the endpoint to test
2. Add test data to `tests/config.yaml` if needed
3. Add test to appropriate file or create new file
4. Use markers: `@pytest.mark.api`, `@pytest.mark.ui`, etc.
5. Run test: `pytest path/to/test.py::TestClass::test_method -v`

Example:

```python
import pytest

class TestNewFeature:
    @pytest.mark.api
    def test_new_endpoint(self, session, base_url, timeout):
        """Test new endpoint."""
        url = f"{base_url}/new/endpoint"
        response = session.get(url, timeout=timeout)
        assert response.status_code == 200
```

### Debugging Tests

```bash
# Show detailed output
pytest test_family.py -vv

# Show print statements
pytest test_family.py -s

# Drop into debugger on failure
pytest test_family.py --pdb

# Show local variables
pytest test_family.py -l
```

## 📦 Dependencies

- **pytest** - Testing framework
- **requests** - HTTP client
- **pytest-html** - HTML report generation
- **pytest-xdist** - Parallel test execution
- **pytest-timeout** - Test timeout handling
- **pyyaml** - Configuration file parsing
- **beautifulsoup4** - HTML parsing
- **lxml** - XML parsing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new endpoints
4. Update documentation
5. Submit a pull request

## 📄 License

This test suite follows the same license as the Rfam project.

## 📧 Support

- **Issues**: GitHub Issues
- **Email**: rfam-help@ebi.ac.uk
- **Documentation**: https://docs.rfam.org

## 🙏 Acknowledgments

Created to support the Rfam website rewrite from Perl/Catalyst to Django, enabling a systematic TDD approach to ensure feature parity and data consistency.

## 📚 Resources

- **Rfam Website**: https://rfam.org
- **Rfam Documentation**: https://docs.rfam.org
- **Rfam GitHub**: https://github.com/Rfam/rfam-website
- **Rfam FTP**: https://ftp.ebi.ac.uk/pub/databases/Rfam

---

**Note**: This test suite tests the **live production site** at https://rfam.org by default. To test against a development server, modify `tests/config.yaml`.
