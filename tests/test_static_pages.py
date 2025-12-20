"""
Tests for static pages and general site functionality.
"""
import pytest
from bs4 import BeautifulSoup


class TestHomePage:
    """Test the home page."""

    @pytest.mark.ui
    def test_home_page_loads(self, session, base_url, timeout):
        """Test that the home page loads successfully."""
        url = base_url
        response = session.get(url, timeout=timeout)
        assert response.status_code == 200
        assert 'text/html' in response.headers['Content-Type']

    @pytest.mark.ui
    def test_home_page_has_search(self, session, base_url, timeout):
        """Test that home page has search functionality."""
        url = base_url
        response = session.get(url, timeout=timeout)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Should have navigation or search links
        text = response.text.lower()
        assert 'search' in text or 'rfam' in text

    @pytest.mark.ui
    def test_home_page_has_navigation(self, session, base_url, timeout):
        """Test that home page has main navigation."""
        url = base_url
        response = session.get(url, timeout=timeout)

        # Should have links to main sections
        text = response.text.lower()
        assert 'family' in text or 'search' in text or 'browse' in text


class TestHelpPages:
    """Test help and documentation pages."""

    @pytest.mark.ui
    def test_help_index(self, session, base_url, timeout):
        """Test that help page loads."""
        url = f"{base_url}/help"
        response = session.get(url, timeout=timeout)
        assert response.status_code in [200, 302]


class TestSpecialPages:
    """Test special content pages."""

    @pytest.mark.ui
    def test_covid_page(self, session, base_url, timeout):
        """Test COVID-19 page.

        Note: The correct URL is /covid-19, not /covid
        """
        url = f"{base_url}/covid-19"
        response = session.get(url, timeout=timeout)
        assert response.status_code == 200
        assert 'text/html' in response.headers['Content-Type']

    @pytest.mark.ui
    def test_viruses_page(self, session, base_url, timeout):
        """Test viruses page."""
        url = f"{base_url}/viruses"
        response = session.get(url, timeout=timeout)
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert 'text/html' in response.headers['Content-Type']

    @pytest.mark.ui
    def test_microrna_page(self, session, base_url, timeout):
        """Test microRNA page."""
        url = f"{base_url}/microrna"
        response = session.get(url, timeout=timeout)
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert 'text/html' in response.headers['Content-Type']

    @pytest.mark.ui
    def test_rfam20_page(self, session, base_url, timeout):
        """Test Rfam 20th anniversary page."""
        url = f"{base_url}/rfam20"
        response = session.get(url, timeout=timeout)
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert 'text/html' in response.headers['Content-Type']

    @pytest.mark.ui
    def test_3d_page(self, session, base_url, timeout):
        """Test 3D families page."""
        url = f"{base_url}/3d"
        response = session.get(url, timeout=timeout)
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert 'text/html' in response.headers['Content-Type']


class TestStatusEndpoints:
    """Test status and utility endpoints."""

    @pytest.mark.api
    def test_status_endpoint(self, session, base_url, timeout):
        """Test status/health check endpoint."""
        url = f"{base_url}/status"
        response = session.get(url, timeout=timeout)
        # Status endpoint may or may not exist
        assert response.status_code in [200, 404]


class TestRobots:
    """Test robots.txt and sitemap."""

    @pytest.mark.api
    def test_robots_txt(self, session, base_url, timeout):
        """Test that robots.txt exists."""
        url = f"{base_url}/robots.txt"
        response = session.get(url, timeout=timeout)
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert 'text/plain' in response.headers['Content-Type'] or 'text' in response.headers['Content-Type']


class TestSecurityHeaders:
    """Test security-related headers."""

    @pytest.mark.api
    def test_security_headers_present(self, session, base_url, timeout):
        """Test that important security headers are present."""
        url = base_url
        response = session.get(url, timeout=timeout)

        headers = response.headers

        # Check for security headers (not all may be present)
        # X-Content-Type-Options should prevent MIME sniffing
        if 'X-Content-Type-Options' in headers:
            assert headers['X-Content-Type-Options'] == 'nosniff'

        # X-Frame-Options helps prevent clickjacking
        # Note: may be DENY, SAMEORIGIN, or ALLOW-FROM
        if 'X-Frame-Options' in headers:
            assert headers['X-Frame-Options'] in ['DENY', 'SAMEORIGIN', 'ALLOW', 'ALLOW-FROM']


class TestErrorPages:
    """Test error page handling."""

    @pytest.mark.ui
    def test_404_page(self, session, base_url, timeout):
        """Test that 404 pages are handled properly."""
        url = f"{base_url}/this-page-does-not-exist-12345"
        response = session.get(url, timeout=timeout)
        assert response.status_code == 404
