# Rfam Website Test Suite

Comprehensive test suite for auditing the Rfam website (https://rfam.org/) to support Test-Driven Development (TDD) for the Django rewrite.

## Overview

This test suite provides extensive coverage of the Rfam website's functionality, including:

- **Family pages** - Rfam family entities (RF accessions)
- **Clan pages** - Clan groupings (CL accessions)
- **Genome pages** - Genome annotations (NCBI taxonomy IDs)
- **Motif pages** - Structural motifs (RM accessions)
- **Browse functionality** - Browse families, clans, genomes, motifs by various criteria
- **Search functionality** - Sequence search, keyword search, taxonomy search, type search
- **API endpoints** - JSON and XML APIs
- **Data exports** - Alignments in multiple formats, tree data, GFF files
- **Static pages** - Home, help, special content pages (COVID-19, viruses, microRNA)
- **Integration tests** - Complete workflows

## Test Organization

```
tests/
├── conftest.py                    # Shared fixtures and configuration
├── config.yaml                    # Test configuration and test data
├── requirements.txt               # Python dependencies
├── pytest.ini                     # Pytest configuration
├── test_family.py                 # Family page and API tests
├── test_clan.py                   # Clan page tests
├── test_genome.py                 # Genome page tests
├── test_motif.py                  # Motif page tests
├── test_browse.py                 # Browse functionality tests
├── test_search.py                 # Search functionality tests
├── test_static_pages.py           # Static and special pages
├── test_sequence.py               # Sequence and accession tests
├── test_alignment_formats.py      # Alignment export tests
├── test_species_tree.py           # Tree visualization tests
├── test_integration.py            # End-to-end workflow tests
├── README.md                      # This file
├── QUICKSTART.md                  # Quick start guide
├── ENDPOINTS.md                   # Complete endpoint reference
└── KNOWN_ISSUES.md                # Known issues with live site
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Rfam/rfam-website.git
cd rfam-website
```

2. Install test dependencies:
```bash
cd tests
pip install -r requirements.txt
```

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test Files

```bash
# Test only family endpoints
pytest test_family.py

# Test only search functionality
pytest test_search.py

# Test only API endpoints
pytest test_alignment_formats.py
```

### Run Tests by Marker

```bash
# Run only UI tests
pytest -m ui

# Run only API tests
pytest -m api

# Run only search tests
pytest -m search

# Exclude slow tests
pytest -m "not slow"

# Run only integration tests
pytest -m integration
```

### Run Tests in Parallel

```bash
# Run with 4 parallel workers
pytest -n 4
```

### Generate HTML Report

```bash
pytest --html=report.html --self-contained-html
```

### Verbose Output

```bash
pytest -v
```

### Show Test Coverage

```bash
pytest --cov=. --cov-report=html
```

## Configuration

### Test Configuration (config.yaml)

The `config.yaml` file contains:

- **base_url**: Target URL for testing (default: https://rfam.org)
- **timeout**: Request timeout settings
- **test_data**: Sample accessions and IDs for testing
  - Families (RF accessions)
  - Clans (CL accessions)
  - Genomes (NCBI taxonomy IDs)
  - Motifs (RM accessions)
- **alignment_formats**: Supported alignment export formats
- **browse_endpoints**: Browse URLs to test
- **search_sequences**: Test sequences for search functionality

You can modify `config.yaml` to:
- Test against a different URL (e.g., staging environment)
- Add more test data
- Adjust timeouts
- Customize test parameters

### Pytest Configuration (pytest.ini)

The `pytest.ini` file configures:
- Test discovery patterns
- Markers for organizing tests
- Output formatting
- Timeout settings

## Test Markers

Tests are organized with the following markers:

- `@pytest.mark.ui` - User interface/HTML tests
- `@pytest.mark.api` - API endpoint tests
- `@pytest.mark.search` - Search functionality tests
- `@pytest.mark.integration` - End-to-end workflow tests
- `@pytest.mark.slow` - Tests that take longer to run

## Test Categories

### 1. Family Tests (test_family.py)

- HTML pages by accession and ID
- JSON API structure and content
- XML API structure and content
- Data endpoints (alignment, tree, CM, regions)
- Image endpoints (secondary structure, thumbnails)
- Error handling (404s)

**Key endpoints tested:**
- `/family/{acc}` (HTML, JSON, XML)
- `/family/{acc}/alignment`
- `/family/{acc}/tree`
- `/family/{acc}/cm`
- `/family/{acc}/regions`
- `/family/{acc}/structures`
- `/family/{acc}/image`

### 2. Clan Tests (test_clan.py)

- HTML pages by accession and ID
- XML API
- Clan membership
- Structure mappings

**Key endpoints tested:**
- `/clan/{acc}` (HTML, XML)
- `/clan/{acc}/structures`

### 3. Genome Tests (test_genome.py)

- HTML pages by NCBI taxonomy ID
- GFF file downloads
- Browse by kingdom (Bacteria, Eukaryota, Archaea, Viruses)

**Key endpoints tested:**
- `/genome/{ncbi_id}`
- `/genome/{ncbi_id}/gff/{auto_genome}`
- `/genomes`
- `/genomes/{kingdom}`

### 4. Motif Tests (test_motif.py)

- HTML pages by accession and ID
- XML API
- Motif browsing

**Key endpoints tested:**
- `/motif/{acc}` (HTML, XML)
- `/motifs`

### 5. Browse Tests (test_browse.py)

- Browse index page
- Browse families (all, by letter, with structures, top 20)
- Browse clans
- Browse genomes (all, by kingdom)
- Browse motifs

**Key endpoints tested:**
- `/browse`
- `/families`, `/families/{letter}`, `/families/with_structure`, `/families/top20`
- `/clans`
- `/genomes`, `/genomes/{kingdom}`
- `/motifs`

### 6. Search Tests (test_search.py)

- Search index page
- Sequence search (single and batch)
- Keyword search
- Taxonomy search
- Type search
- Jump/smart search

**Key endpoints tested:**
- `/search`
- `/search/sequence` (POST and GET)
- `/search/batch`
- `/search/keyword`
- `/search/taxonomy`
- `/search/type`
- `/jump`

### 7. Static Pages Tests (test_static_pages.py)

- Home page
- Help pages
- Special content pages (COVID-19, viruses, microRNA, Rfam 20)
- Status endpoints
- Security headers
- Error pages (404)

**Key endpoints tested:**
- `/`
- `/help`
- `/covid`, `/viruses`, `/microrna`, `/rfam20`, `/3d`
- `/status`
- `/robots.txt`

### 8. Sequence Tests (test_sequence.py)

- Sequence hit pages
- Accession lookups
- Structure downloads

**Key endpoints tested:**
- `/sequence/{accession}`
- `/sequence/{accession}/hits`
- `/accession/{accession}`
- `/structure/{pdb_id}`

### 9. Alignment Format Tests (test_alignment_formats.py)

- Alignment exports in multiple formats (Stockholm, Pfam, FASTA, Clustal, Phylip, PSI-BLAST)
- Tree data downloads
- Region data

**Key endpoints tested:**
- `/family/{acc}/alignment?format={format}`
- `/family/{acc}/tree/data`
- `/family/{acc}/tree/image`
- `/family/{acc}/regions`
- `/family/{acc}/refseq`

### 10. Integration Tests (test_integration.py)

- Complete workflows (browse → family → data export)
- Search to family workflows
- API consistency (JSON vs XML)
- Cross-linking between entities
- Data export workflows

## Expected Test Results

### Successful Tests
Tests that pass indicate the endpoint:
- Returns expected HTTP status code
- Contains expected content type
- Includes required data fields
- Handles errors appropriately

### Tests That May Fail
Some tests may legitimately fail if:
- Features are deprecated or removed
- Endpoints have changed URL structure
- Data is not available for test entities
- Rate limiting is enforced

These failures help identify what needs attention in the Django rewrite.

## Continuous Integration

### GitHub Actions

A sample GitHub Actions workflow is provided in `.github/workflows/test.yml` (if created).

To run tests automatically on every commit:

```yaml
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd tests
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd tests
          pytest --html=report.html --self-contained-html
      - name: Upload test report
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: test-report
          path: tests/report.html
```

## Using Tests for Django Rewrite

### TDD Workflow

1. **Run tests against current site** - Establish baseline
```bash
pytest --html=baseline-report.html
```

2. **Implement Django endpoint** - Create your Django view/API

3. **Update config.yaml** - Point to Django development server
```yaml
base_url: "http://localhost:8000"
```

4. **Run tests against Django** - Verify behavior matches
```bash
pytest --html=django-report.html
```

5. **Fix failing tests** - Iterate until Django matches Perl/Catalyst behavior

6. **Repeat** for each endpoint

### Test-First Approach

For each Django endpoint:

1. Review corresponding test in this suite
2. Understand expected behavior
3. Implement Django view/API
4. Run specific test: `pytest test_family.py::TestFamilyPages::test_family_page_by_accession`
5. Debug until test passes
6. Move to next endpoint

## Troubleshooting

### Timeout Errors

If tests timeout, increase timeout in `config.yaml`:
```yaml
timeout: 60
long_timeout: 120
```

### Connection Errors

Check network connectivity:
```bash
curl -I https://rfam.org
```

Test with a different base URL:
```yaml
base_url: "http://rfam.org"  # Try HTTP instead of HTTPS
```

### Rate Limiting

If hitting rate limits, run fewer tests in parallel:
```bash
pytest -n 1  # Run sequentially
```

Or add delays between requests in `conftest.py`.

### SSL Errors

If encountering SSL certificate errors:
```python
# In conftest.py, modify session fixture
s.verify = False  # Disable SSL verification (not recommended for production)
```

## Contributing

When adding new tests:

1. Follow existing test structure and naming conventions
2. Add appropriate markers (`@pytest.mark.ui`, `@pytest.mark.api`, etc.)
3. Document expected behavior
4. Add test data to `config.yaml` if needed
5. Update this README with new test categories

## Test Data

The test suite uses real Rfam accessions that should be stable:

- **RF00001** (5S_rRNA) - Small, well-known family
- **RF00005** (tRNA) - Belongs to clan CL00001
- **CL00001** (tRNA clan) - Has multiple member families
- **511145** (E. coli K-12) - Model organism genome

If these accessions change or are removed, update `config.yaml`.

## Performance

### Benchmark

On a typical system with good internet connection:
- **Full suite**: ~5-10 minutes (with parallelization)
- **Fast tests only** (`-m "not slow"`): ~2-3 minutes
- **Single test file**: ~10-30 seconds

### Optimization

To run faster:
```bash
# Maximum parallelization
pytest -n auto

# Skip slow tests
pytest -m "not slow"

# Fail fast (stop on first failure)
pytest -x

# Run only failed tests from last run
pytest --lf
```

## License

This test suite is part of the Rfam project and follows the same license as the main repository.

## Support

For questions or issues:
- Open an issue on GitHub
- Contact: rfam-help@ebi.ac.uk
- Documentation: https://docs.rfam.org

## Acknowledgments

This test suite was created to support the Rfam website rewrite from Perl/Catalyst to Django, enabling a TDD approach to ensure feature parity and data consistency.
