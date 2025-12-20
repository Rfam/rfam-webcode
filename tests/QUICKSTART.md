# Quick Start Guide

Get up and running with the Rfam test suite in 5 minutes.

## Prerequisites

- Python 3.8+
- Internet connection (tests run against live https://rfam.org)

## 1. Install Dependencies

```bash
cd tests
pip install -r requirements.txt
```

Or use the convenience script to create a virtual environment:

```bash
./run_tests.sh --help
```

## 2. Run Your First Tests

### Quick Test (Fast Tests Only)

```bash
pytest -m "not slow" -v
```

This runs the fast tests and should complete in 2-3 minutes.

### Run All Tests

```bash
pytest
```

Or use the script:

```bash
./run_tests.sh
```

### Run Specific Test Categories

```bash
# Test only family endpoints
pytest test_family.py -v

# Test only search functionality
pytest test_search.py -v

# Test only API endpoints
pytest -m api -v
```

## 3. Generate HTML Report

```bash
pytest --html=report.html --self-contained-html
```

Then open `report.html` in your browser.

Or use the script:

```bash
./run_tests.sh --report
```

## 4. Run Tests in Parallel (Faster)

```bash
pytest -n 4  # Use 4 parallel workers
```

Or:

```bash
pytest -n auto  # Automatically detect number of CPUs
```

Or use the script:

```bash
./run_tests.sh --parallel
```

## 5. Understanding Test Results

### ✅ Passed Tests
These endpoints work as expected on the live site.

### ❌ Failed Tests
These indicate:
- Endpoint behavior changed
- Endpoint no longer exists
- Rate limiting
- Network issues
- Data changes (e.g., test family was removed)

Failed tests help identify what needs attention in your Django rewrite.

### ⚠️ Skipped Tests
Currently, there are no skipped tests, but some tests check for `status_code in [200, 404]` to handle endpoints that may not be deployed.

## Common Test Commands

```bash
# Run fast tests only
pytest -m "not slow"

# Run UI tests
pytest -m ui

# Run API tests
pytest -m api

# Run search tests
pytest -m search

# Run a specific test
pytest test_family.py::TestFamilyPages::test_family_page_by_accession

# Stop on first failure
pytest -x

# Show detailed output
pytest -vv

# Run with coverage
pytest --cov=. --cov-report=html
```

## Using for TDD with Django

### Step 1: Establish Baseline

Run tests against the current Perl/Catalyst site:

```bash
pytest --html=baseline-report.html --self-contained-html
```

Save this report as your baseline.

### Step 2: Configure for Django

Edit `config.yaml`:

```yaml
base_url: "http://localhost:8000"  # Your Django dev server
```

### Step 3: Test Against Django

Start your Django server, then:

```bash
pytest --html=django-report.html --self-contained-html
```

### Step 4: Compare Reports

Compare `baseline-report.html` with `django-report.html` to see:
- Which endpoints match
- Which need work
- What data structure differences exist

### Step 5: Iterate

For each failing test:
1. Review the test to understand expected behavior
2. Fix your Django implementation
3. Rerun the specific test: `pytest test_family.py::TestFamilyPages::test_family_page_by_accession -v`
4. Repeat until passing

## Test Development Workflow

### Testing a Single Endpoint

```bash
# Run just family accession tests
pytest test_family.py::TestFamilyPages::test_family_page_by_accession -v

# Run all family page tests
pytest test_family.py::TestFamilyPages -v

# Run all family tests
pytest test_family.py -v
```

### Adding New Tests

1. Identify the endpoint you want to test
2. Add test data to `config.yaml` if needed
3. Create test in appropriate file (e.g., `test_family.py`)
4. Run the new test: `pytest path/to/test.py::TestClass::test_method -v`

### Debugging Failed Tests

```bash
# Show more detail
pytest test_family.py -vv

# Show print statements
pytest test_family.py -s

# Drop into debugger on failure
pytest test_family.py --pdb

# Show local variables on failure
pytest test_family.py -l
```

## Troubleshooting

### Tests Timeout

Increase timeout in `config.yaml`:

```yaml
timeout: 60
long_timeout: 120
```

### Connection Errors

Check that https://rfam.org is accessible:

```bash
curl -I https://rfam.org
```

### Too Many Failures

Run fast tests only:

```bash
pytest -m "not slow" --maxfail=5
```

This stops after 5 failures.

### Rate Limiting

Run tests sequentially:

```bash
pytest -n 1
```

Or add delays in `conftest.py`.

## Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Review [ENDPOINTS.md](ENDPOINTS.md) for complete endpoint reference
3. Check test files for examples of testing patterns
4. Start implementing your Django endpoints!

## Quick Reference

| Command | Purpose |
|---------|---------|
| `pytest` | Run all tests |
| `pytest -v` | Verbose output |
| `pytest -x` | Stop on first failure |
| `pytest -m "not slow"` | Skip slow tests |
| `pytest -m api` | API tests only |
| `pytest -n auto` | Parallel execution |
| `pytest --html=report.html` | Generate HTML report |
| `./run_tests.sh --help` | See all script options |

## Support

- Issues: GitHub Issues
- Email: rfam-help@ebi.ac.uk
- Docs: https://docs.rfam.org

Happy testing! 🧪
