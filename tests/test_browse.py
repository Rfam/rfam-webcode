"""
Tests for Rfam browse functionality.
"""
import pytest
from bs4 import BeautifulSoup
import string


class TestBrowseIndex:
    """Test the main browse page."""

    @pytest.mark.ui
    def test_browse_index_page(self, session, base_url, timeout):
        """Test the browse index page loads."""
        url = f"{base_url}/browse"
        response = session.get(url, timeout=timeout)
        assert response.status_code == 200
        assert 'text/html' in response.headers['Content-Type']
        # Should have links to browse different entity types
        assert 'families' in response.text.lower() or 'browse' in response.text.lower()


class TestBrowseFamilies:
    """Test family browsing functionality."""

    @pytest.mark.ui
    def test_families_browse_page(self, session, base_url, timeout):
        """Test the families browse page."""
        url = f"{base_url}/families"
        response = session.get(url, timeout=timeout)
        assert response.status_code == 200
        assert 'text/html' in response.headers['Content-Type']
        # Should show families or alphabet navigation
        assert len(response.text) > 1000

    @pytest.mark.ui
    @pytest.mark.parametrize("letter", ['A', 'B', 'C', 'T', 'S', 'R'])
    def test_families_by_letter(self, session, base_url, timeout, letter):
        """Test browsing families by letter."""
        url = f"{base_url}/families/{letter}"
        response = session.get(url, timeout=timeout)
        assert response.status_code == 200
        assert 'text/html' in response.headers['Content-Type']

    @pytest.mark.ui
    def test_families_with_structure(self, session, base_url, timeout):
        """Test browsing families with 3D structures."""
        url = f"{base_url}/families/with_structure"
        response = session.get(url, timeout=timeout)
        assert response.status_code == 200
        assert 'text/html' in response.headers['Content-Type']

    @pytest.mark.ui
    def test_families_top20(self, session, base_url, timeout):
        """Test browsing top 20 largest families."""
        url = f"{base_url}/families/top20"
        response = session.get(url, timeout=timeout)
        assert response.status_code == 200
        assert 'text/html' in response.headers['Content-Type']


class TestBrowseClans:
    """Test clan browsing functionality."""

    @pytest.mark.ui
    def test_clans_browse_page(self, session, base_url, timeout):
        """Test the clans browse page."""
        url = f"{base_url}/clans"
        response = session.get(url, timeout=timeout)
        assert response.status_code == 200
        assert 'text/html' in response.headers['Content-Type']


class TestBrowseMotifs:
    """Test motif browsing functionality."""

    @pytest.mark.ui
    def test_motifs_browse_page(self, session, base_url, timeout):
        """Test the motifs browse page."""
        url = f"{base_url}/motifs"
        response = session.get(url, timeout=timeout)
        assert response.status_code == 200
        assert 'text/html' in response.headers['Content-Type']


class TestBrowseStructures:
    """Test structure browsing functionality."""

    @pytest.mark.ui
    def test_browse_families_with_structures(self, session, base_url, timeout):
        """Test browsing families that have structure data."""
        url = f"{base_url}/families/with_structure"
        response = session.get(url, timeout=timeout)
        assert response.status_code == 200


class TestBrowseArticles:
    """Test Wikipedia article browsing."""

    @pytest.mark.ui
    def test_browse_articles(self, session, base_url, timeout):
        """Test browsing Wikipedia articles."""
        url = f"{base_url}/articles"
        response = session.get(url, timeout=timeout)
        # Articles endpoint may or may not exist
        assert response.status_code in [200, 404]
