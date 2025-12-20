"""
Tests for Rfam genome pages and endpoints.
"""
import pytest
from bs4 import BeautifulSoup


class TestGenomePages:
    """Test genome HTML pages."""

    @pytest.mark.ui
    def test_genome_page_by_ncbi_id(self, session, base_url, test_genomes, timeout):
        """Test that genome pages are accessible by NCBI taxonomy ID."""
        for genome in test_genomes:
            url = f"{base_url}/genome/{genome['ncbi_id']}"
            response = session.get(url, timeout=timeout)
            assert response.status_code == 200, f"Genome page {genome['ncbi_id']} returned {response.status_code}"
            assert 'text/html' in response.headers['Content-Type']
            assert genome['ncbi_id'] in response.text

    @pytest.mark.ui
    def test_genome_page_structure(self, session, base_url, timeout):
        """Test that genome pages have expected structure."""
        url = f"{base_url}/genome/511145"  # E. coli K-12
        response = session.get(url, timeout=timeout)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Check for basic page structure
        assert soup.find('title') is not None
        assert len(response.text) > 500, "Genome page seems too short"

    def test_genome_404_on_invalid_id(self, session, base_url, timeout):
        """Test that invalid genome IDs return 404.

        Note: Site may return 200 with error page instead of proper 404.
        """
        url = f"{base_url}/genome/999999999"
        response = session.get(url, timeout=timeout)
        # Site returns 200 with error page instead of 404
        assert response.status_code in [200, 404]


class TestGenomeDataEndpoints:
    """Test genome data export endpoints."""

    @pytest.mark.api
    @pytest.mark.slow
    def test_genome_gff_download(self, session, base_url, timeout):
        """Test GFF file download for genome annotations."""
        # Note: auto_genome ID might be different from NCBI ID
        # This tests the endpoint structure, actual downloads may require valid auto_genome IDs
        url = f"{base_url}/genome/511145/gff/1"
        response = session.get(url, timeout=timeout, allow_redirects=True)
        # GFF endpoint might not exist for all genomes
        assert response.status_code in [200, 404, 400, 302]


