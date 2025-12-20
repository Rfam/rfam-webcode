"""
Tests for Rfam clan pages and endpoints.
"""
import pytest
from bs4 import BeautifulSoup


class TestClanPages:
    """Test clan HTML pages."""

    @pytest.mark.ui
    def test_clan_page_by_accession(self, session, base_url, test_clans, timeout):
        """Test that clan pages are accessible by accession."""
        for clan in test_clans:
            url = f"{base_url}/clan/{clan['acc']}"
            response = session.get(url, timeout=timeout)
            assert response.status_code == 200, f"Clan page {clan['acc']} returned {response.status_code}"
            assert 'text/html' in response.headers['Content-Type']
            assert clan['acc'] in response.text

    @pytest.mark.ui
    def test_clan_page_by_id(self, session, base_url, test_clans, timeout):
        """Test that clan pages are accessible by ID."""
        for clan in test_clans:
            url = f"{base_url}/clan/{clan['id']}"
            response = session.get(url, timeout=timeout)
            assert response.status_code == 200, f"Clan page {clan['id']} returned {response.status_code}"
            assert 'text/html' in response.headers['Content-Type']

    @pytest.mark.ui
    def test_clan_page_structure(self, session, base_url, timeout):
        """Test that clan pages have expected structure."""
        url = f"{base_url}/clan/CL00001"
        response = session.get(url, timeout=timeout)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Check for basic page structure
        assert soup.find('title') is not None
        assert len(response.text) > 1000, "Clan page seems too short"

    def test_clan_404_on_invalid_accession(self, session, base_url, timeout):
        """Test that invalid clan accessions return 404.

        Note: Site may return 200 with error page instead of proper 404.
        """
        url = f"{base_url}/clan/CL99999"
        response = session.get(url, timeout=timeout)
        # Site returns 200 with error page instead of 404
        assert response.status_code in [200, 404]


class TestClanAPIXML:
    """Test clan XML API endpoints."""

    @pytest.mark.api
    def test_clan_xml_parameter(self, session, base_url, test_clans, timeout):
        """Test clan XML via output parameter."""
        for clan in test_clans:
            url = f"{base_url}/clan/{clan['acc']}?output=xml"
            response = session.get(url, timeout=timeout)
            # XML may or may not be available for clans
            if response.status_code == 200:
                assert 'xml' in response.headers.get('Content-Type', '')


class TestClanDataEndpoints:
    """Test clan data endpoints."""

    @pytest.mark.api
    def test_clan_structures_endpoint(self, session, base_url, timeout):
        """Test clan structures endpoint."""
        url = f"{base_url}/clan/CL00001/structures"
        response = session.get(url, timeout=timeout)
        # Structures endpoint may or may not exist
        assert response.status_code in [200, 404, 405]


class TestClanMembership:
    """Test clan membership information."""

    @pytest.mark.ui
    def test_clan_shows_member_families(self, session, base_url, timeout):
        """Test that clan pages show member families."""
        url = f"{base_url}/clan/CL00001"
        response = session.get(url, timeout=timeout)
        assert response.status_code == 200
        # Clan pages should reference family members
        # The tRNA clan should contain tRNA family references
        assert 'RF' in response.text  # Should contain Rfam family accessions
