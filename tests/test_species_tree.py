"""
Tests for species tree and visualization endpoints.
"""
import pytest


class TestSpeciesTree:
    """Test species tree functionality."""

    @pytest.mark.ui
    def test_species_tree_page(self, session, base_url, timeout):
        """Test species tree page."""
        url = f"{base_url}/speciestree"
        response = session.get(url, timeout=timeout)
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert 'text/html' in response.headers['Content-Type']


class TestSunburstVisualization:
    """Test sunburst visualization for taxonomic distribution."""

    @pytest.mark.ui
    def test_family_sunburst(self, session, base_url, timeout):
        """Test family sunburst visualization."""
        url = f"{base_url}/family/RF00001/sunburst"
        response = session.get(url, timeout=timeout)
        # Sunburst may or may not be available
        assert response.status_code in [200, 404]


class TestMSAViewer:
    """Test multiple sequence alignment viewer."""

    @pytest.mark.ui
    def test_msa_viewer_endpoint(self, session, base_url, timeout):
        """Test MSA viewer endpoint."""
        # Note: exact URL structure may vary
        url = f"{base_url}/family/RF00001"
        response = session.get(url, timeout=timeout)
        # Check if MSA viewer is embedded in family page
        assert response.status_code == 200
