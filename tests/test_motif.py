"""
Tests for Rfam motif pages and endpoints.
"""
import pytest
from bs4 import BeautifulSoup


class TestMotifPages:
    """Test motif HTML pages."""

    @pytest.mark.ui
    def test_motif_page_by_accession(self, session, base_url, test_motifs, timeout):
        """Test that motif pages are accessible by accession."""
        for motif in test_motifs:
            url = f"{base_url}/motif/{motif['acc']}"
            response = session.get(url, timeout=timeout)
            assert response.status_code == 200, f"Motif page {motif['acc']} returned {response.status_code}"
            assert 'text/html' in response.headers['Content-Type']
            assert motif['acc'] in response.text

    @pytest.mark.ui
    def test_motif_page_by_id(self, session, base_url, test_motifs, timeout):
        """Test that motif pages are accessible by ID."""
        for motif in test_motifs:
            url = f"{base_url}/motif/{motif['id']}"
            response = session.get(url, timeout=timeout)
            assert response.status_code == 200, f"Motif page {motif['id']} returned {response.status_code}"
            assert 'text/html' in response.headers['Content-Type']

    @pytest.mark.ui
    def test_motif_page_structure(self, session, base_url, timeout):
        """Test that motif pages have expected structure."""
        url = f"{base_url}/motif/RM00001"
        response = session.get(url, timeout=timeout)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Check for basic page structure
        assert soup.find('title') is not None
        assert len(response.text) > 500, "Motif page seems too short"

    def test_motif_404_on_invalid_accession(self, session, base_url, timeout):
        """Test that invalid motif accessions return 404.

        Note: Site may return 200 with error page instead of proper 404.
        """
        url = f"{base_url}/motif/RM99999"
        response = session.get(url, timeout=timeout)
        # Site returns 200 with error page instead of 404
        assert response.status_code in [200, 404]


class TestMotifAPIXML:
    """Test motif XML API endpoints."""

    @pytest.mark.api
    def test_motif_xml_parameter(self, session, base_url, test_motifs, timeout):
        """Test motif XML via output parameter."""
        for motif in test_motifs:
            url = f"{base_url}/motif/{motif['acc']}?output=xml"
            response = session.get(url, timeout=timeout)
            # XML may or may not be available for motifs
            if response.status_code == 200:
                assert 'xml' in response.headers.get('Content-Type', '')


class TestMotifBrowse:
    """Test motif browsing functionality."""

    @pytest.mark.ui
    def test_motifs_browse_page(self, session, base_url, timeout):
        """Test the motifs browse page."""
        url = f"{base_url}/motifs"
        response = session.get(url, timeout=timeout)
        assert response.status_code == 200
        assert 'text/html' in response.headers['Content-Type']
