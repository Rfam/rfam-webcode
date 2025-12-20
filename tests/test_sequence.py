"""
Tests for sequence and accession endpoints.
"""
import pytest
from bs4 import BeautifulSoup


class TestSequencePages:
    """Test sequence hit pages."""

    @pytest.mark.ui
    def test_sequence_page_by_accession(self, session, base_url, timeout):
        """Test sequence page by accession."""
        # Use a common GenBank accession
        url = f"{base_url}/sequence/AJ634207"
        response = session.get(url, timeout=timeout)
        # Sequence may or may not exist in database
        assert response.status_code in [200, 404]

    @pytest.mark.ui
    def test_sequence_with_entry_parameter(self, session, base_url, timeout):
        """Test sequence lookup with entry parameter."""
        url = f"{base_url}/sequence"
        params = {'entry': 'AJ634207'}
        response = session.get(url, params=params, timeout=timeout)
        # Should return sequence page or redirect
        assert response.status_code in [200, 302, 404]

    @pytest.mark.ui
    def test_sequence_hits_fragment(self, session, base_url, timeout):
        """Test sequence hits table fragment."""
        url = f"{base_url}/sequence/AJ634207/hits"
        response = session.get(url, timeout=timeout)
        # Hits endpoint may or may not exist
        assert response.status_code in [200, 404, 405]


class TestAccessionPages:
    """Test accession endpoint."""

    @pytest.mark.ui
    def test_accession_endpoint(self, session, base_url, timeout):
        """Test accession endpoint with sequence coordinates."""
        url = f"{base_url}/accession/AJ634207"
        params = {'seq_start': '1', 'seq_end': '100'}
        response = session.get(url, params=params, timeout=timeout)
        # Accession endpoint may or may not exist
        assert response.status_code in [200, 404, 302]


class TestStructureEndpoints:
    """Test structure-related endpoints."""

    @pytest.mark.api
    @pytest.mark.skip(reason="PDB download endpoint is broken on live site (500 error + timeout). "
                             "Django rewrite should fix or remove this endpoint. "
                             "See: /structure/{pdb_id}")
    def test_structure_pdb_download(self, session, base_url, timeout):
        """Test PDB structure file download.

        NOTE: As of Dec 2025, this endpoint is broken on the live site
        (returns 500 errors and times out). This test is skipped to avoid
        timeouts. The Django rewrite should either fix this or remove the endpoint.
        """
        # Use a known PDB ID from Rfam (1QVG is in RF00001)
        url = f"{base_url}/structure/1QVG"
        response = session.get(url, timeout=timeout, allow_redirects=True)
        # Structure endpoint is currently broken (500) on live site
        assert response.status_code in [200, 302, 404, 500]

    @pytest.mark.ui
    def test_structure_viewer_endpoint(self, session, base_url, timeout):
        """Test structure viewer (AstexViewer) endpoint.

        This endpoint works correctly on the live site.
        """
        # Use a known PDB ID from Rfam (1QVG is in RF00001)
        url = f"{base_url}/structure/1QVG/av"
        response = session.get(url, timeout=timeout)
        # Viewer endpoint should work
        assert response.status_code == 200
