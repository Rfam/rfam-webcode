"""
Pytest configuration and shared fixtures for Rfam test suite.
"""
import pytest
import requests
import yaml
from pathlib import Path


@pytest.fixture(scope="session")
def config():
    """Load test configuration from config.yaml."""
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def base_url(config):
    """Get the base URL for the Rfam website."""
    return config['base_url']


@pytest.fixture(scope="session")
def timeout(config):
    """Get the default timeout for requests."""
    return config['timeout']


@pytest.fixture(scope="session")
def session():
    """Create a requests session for reusing connections."""
    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Rfam-TDD-Test-Suite/1.0'
    })
    return s


@pytest.fixture
def test_families(config):
    """Get list of test families."""
    return config['test_data']['families']


@pytest.fixture
def test_clans(config):
    """Get list of test clans."""
    return config['test_data']['clans']


@pytest.fixture
def test_genomes(config):
    """Get list of test genomes."""
    return config['test_data']['genomes']


@pytest.fixture
def test_motifs(config):
    """Get list of test motifs."""
    return config['test_data']['motifs']


@pytest.fixture
def alignment_formats(config):
    """Get list of alignment formats to test."""
    return config['alignment_formats']


@pytest.fixture
def content_types(config):
    """Get content types to test."""
    return config['content_types']


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "api: marks tests as API tests"
    )
    config.addinivalue_line(
        "markers", "ui: marks tests as UI/HTML tests"
    )
    config.addinivalue_line(
        "markers", "search: marks tests as search functionality tests"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
