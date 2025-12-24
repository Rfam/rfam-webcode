"""
Tests for visualization endpoints.
"""
import pytest


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
