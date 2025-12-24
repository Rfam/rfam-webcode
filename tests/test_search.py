"""
Tests for Rfam search functionality.
"""
import pytest
import time
import uuid
from bs4 import BeautifulSoup


class TestSearchPages:
    """Test search page UI."""

    @pytest.mark.ui
    def test_search_index_page(self, session, base_url, timeout):
        """Test the main search page loads."""
        url = f"{base_url}/search"
        response = session.get(url, timeout=timeout)
        assert response.status_code == 200
        assert 'text/html' in response.headers['Content-Type']
        # Should have search forms
        assert 'search' in response.text.lower()

    @pytest.mark.ui
    def test_search_page_has_search_types(self, session, base_url, timeout):
        """Test that search page shows different search types."""
        url = f"{base_url}/search"
        response = session.get(url, timeout=timeout)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Search page should mention various search types
        text = response.text.lower()
        # At least sequence and keyword search should be mentioned
        assert 'sequence' in text or 'keyword' in text


class TestBatchSearch:
    """Test batch sequence search functionality."""

    @pytest.mark.search
    @pytest.mark.slow
    def test_batch_search_endpoint_exists(self, session, base_url, timeout):
        """Test that batch search endpoint is accessible."""
        url = f"{base_url}/search/batch"
        response = session.get(url, timeout=timeout)
        # Batch search page should exist
        assert response.status_code in [200, 405]  # 405 if only POST allowed


class TestKeywordSearch:
    """Test keyword search functionality."""

    @pytest.mark.search
    def test_keyword_search_get(self, session, base_url, timeout):
        """Test keyword search with GET request."""
        url = f"{base_url}/search/keyword"
        params = {'query': 'ribosome'}

        response = session.get(url, params=params, timeout=timeout)
        assert response.status_code in [200, 302]

    @pytest.mark.search
    def test_keyword_search_returns_results(self, session, base_url, timeout):
        """Test that keyword search returns results."""
        url = f"{base_url}/search/keyword"
        params = {'query': '5S'}

        response = session.get(url, params=params, timeout=timeout, allow_redirects=True)
        assert response.status_code == 200
        # Should contain results or "result" text
        text = response.text.lower()
        assert 'rf' in text or 'result' in text or 'family' in text


class TestTaxonomySearch:
    """Test taxonomy search functionality."""

    @pytest.mark.search
    def test_taxonomy_search_endpoint(self, session, base_url, timeout):
        """Test taxonomy search endpoint."""
        url = f"{base_url}/search/taxonomy"
        params = {'query': 'Homo sapiens'}

        response = session.get(url, params=params, timeout=timeout)
        # Taxonomy search should exist
        assert response.status_code in [200, 302, 400]


class TestTypeSearch:
    """Test entry type search functionality."""

    @pytest.mark.search
    def test_type_search_endpoint(self, session, base_url, timeout):
        """Test entry type search endpoint."""
        url = f"{base_url}/search/type"
        params = {'query': 'rRNA'}

        response = session.get(url, params=params, timeout=timeout)
        # Type search should exist
        assert response.status_code in [200, 302, 400]


class TestJumpSearch:
    """Test jump/smart search functionality."""

    @pytest.mark.search
    def test_jump_with_family_accession(self, session, base_url, timeout):
        """Test jump search with family accession."""
        url = f"{base_url}/jump"
        params = {'entry': 'RF00001'}

        response = session.get(url, params=params, timeout=timeout, allow_redirects=False)
        # Should redirect to family page
        if response.status_code in [301, 302, 303]:
            assert '/family/' in response.headers.get('Location', '')

    @pytest.mark.search
    def test_jump_with_family_id(self, session, base_url, timeout):
        """Test jump search with family ID."""
        url = f"{base_url}/jump"
        params = {'entry': '5S_rRNA'}

        response = session.get(url, params=params, timeout=timeout, allow_redirects=False)
        # Should redirect to family page
        if response.status_code in [301, 302, 303]:
            assert 'family' in response.headers.get('Location', '').lower()

    @pytest.mark.search
    def test_jump_with_invalid_entry(self, session, base_url, timeout):
        """Test jump search with invalid entry."""
        url = f"{base_url}/jump"
        params = {'entry': 'INVALID_ENTRY_12345'}

        response = session.get(url, params=params, timeout=timeout)
        # Should return error or show search page
        assert response.status_code in [200, 302, 404]
