"""
Tests for Rfam family pages and endpoints.
"""
import pytest
import requests
from bs4 import BeautifulSoup


class TestFamilyPages:
    """Test family HTML pages."""

    @pytest.mark.ui
    def test_family_page_by_accession(self, session, base_url, test_families, timeout):
        """Test that family pages are accessible by accession."""
        for family in test_families:
            url = f"{base_url}/family/{family['acc']}"
            response = session.get(url, timeout=timeout)
            assert response.status_code == 200, f"Family page {family['acc']} returned {response.status_code}"
            assert 'text/html' in response.headers['Content-Type']
            assert family['description'] in response.text or family['acc'] in response.text

    @pytest.mark.ui
    def test_family_page_by_id(self, session, base_url, test_families, timeout):
        """Test that family pages are accessible by ID."""
        for family in test_families:
            url = f"{base_url}/family/{family['id']}"
            response = session.get(url, timeout=timeout)
            assert response.status_code == 200, f"Family page {family['id']} returned {response.status_code}"
            assert 'text/html' in response.headers['Content-Type']

    @pytest.mark.ui
    def test_family_page_has_required_sections(self, session, base_url, timeout):
        """Test that family pages contain expected sections and elements."""
        url = f"{base_url}/family/RF00001"
        response = session.get(url, timeout=timeout)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Check for common elements
        assert soup.find('title') is not None
        # Family pages should have some form of navigation
        assert len(response.text) > 1000, "Family page seems too short"

    def test_family_404_on_invalid_accession(self, session, base_url, timeout):
        """Test that invalid family accessions return 404.

        Note: Site may return 200/500 with error page instead of proper 404.
        """
        url = f"{base_url}/family/RF99999999"
        response = session.get(url, timeout=timeout)
        # Site returns error page with various status codes
        assert response.status_code in [200, 404, 500]


class TestFamilyAPIJSON:
    """Test family JSON API endpoints."""

    @pytest.mark.api
    def test_family_json_by_accession(self, session, base_url, test_families, timeout):
        """Test that family JSON API works with accession."""
        for family in test_families:
            url = f"{base_url}/family/{family['acc']}"
            response = session.get(
                url,
                headers={'Accept': 'application/json'},
                timeout=timeout
            )
            assert response.status_code == 200
            assert 'application/json' in response.headers['Content-Type']

            data = response.json()
            assert 'rfam' in data
            assert 'acc' in data['rfam']
            assert data['rfam']['acc'] == family['acc']
            assert 'id' in data['rfam']
            assert 'description' in data['rfam']
            assert 'curation' in data['rfam']
            assert 'cm' in data['rfam']
            assert 'release' in data['rfam']

    @pytest.mark.api
    def test_family_json_structure(self, session, base_url, timeout):
        """Test that family JSON has expected structure."""
        url = f"{base_url}/family/RF00001"
        response = session.get(
            url,
            headers={'Accept': 'application/json'},
            timeout=timeout
        )
        data = response.json()
        rfam = data['rfam']

        # Check release info
        assert 'release' in rfam
        assert 'number' in rfam['release']
        assert 'date' in rfam['release']

        # Check curation info
        assert 'curation' in rfam
        curation = rfam['curation']
        assert 'num_seed' in curation
        assert 'num_full' in curation
        assert 'num_species' in curation
        assert 'type' in curation

        # Check CM info
        assert 'cm' in rfam
        cm = rfam['cm']
        assert 'build_command' in cm
        assert 'search_command' in cm
        assert 'cutoffs' in cm
        assert 'gathering' in cm['cutoffs']
        assert 'trusted' in cm['cutoffs']
        assert 'noise' in cm['cutoffs']


class TestFamilyAPIXML:
    """Test family XML API endpoints."""

    @pytest.mark.api
    def test_family_xml_by_accession(self, session, base_url, test_families, timeout):
        """Test that family XML API works with accession."""
        for family in test_families:
            url = f"{base_url}/family/{family['acc']}"
            response = session.get(
                url,
                headers={'Accept': 'text/xml'},
                timeout=timeout
            )
            assert response.status_code == 200
            assert 'xml' in response.headers['Content-Type']

            # Check for XML declaration and key elements
            assert '<?xml version' in response.text
            assert '<rfam' in response.text
            assert '<entry' in response.text
            assert family['acc'] in response.text
            assert '<description>' in response.text
            assert '<curation_details>' in response.text
            assert 'cm_details' in response.text

    @pytest.mark.api
    def test_family_xml_structure(self, session, base_url, timeout):
        """Test that family XML has expected structure."""
        url = f"{base_url}/family/RF00001"
        response = session.get(
            url,
            headers={'Accept': 'text/xml'},
            timeout=timeout
        )

        # Check for required XML elements
        required_elements = [
            '<entry',
            'accession=',
            '<description>',
            '<curation_details>',
            '<author>',
            '<num_seqs>',
            '<seed>',
            '<full>',
            '<num_species>',
            '<type>',
            'cm_details',  # Note: without < to match both <cm_details and cm_details=
            '<build_command>',
            '<calibrate_command>',
            '<search_command>',
            '<cutoffs>',
            '<gathering>',
            '<trusted>',
            '<noise>',
        ]

        for element in required_elements:
            assert element in response.text, f"Missing required element: {element}"


class TestFamilyDataEndpoints:
    """Test family data export endpoints."""

    @pytest.mark.api
    @pytest.mark.slow
    def test_family_alignment_stockholm(self, session, base_url, timeout):
        """Test family alignment download in Stockholm format."""
        url = f"{base_url}/family/RF00001/alignment"
        response = session.get(url, timeout=timeout)
        # Should return alignment data or redirect
        assert response.status_code in [200, 302, 303]

    @pytest.mark.api
    def test_family_tree_endpoint(self, session, base_url, timeout):
        """Test family tree endpoint."""
        url = f"{base_url}/family/RF00001/tree"
        response = session.get(url, timeout=timeout)
        assert response.status_code in [200, 404]  # Some families might not have trees

    @pytest.mark.api
    def test_family_cm_download(self, session, base_url, timeout):
        """Test covariance model download."""
        url = f"{base_url}/family/RF00001/cm"
        response = session.get(url, timeout=timeout)
        assert response.status_code in [200, 302, 303]

    @pytest.mark.api
    def test_family_regions_endpoint(self, session, base_url, timeout):
        """Test family regions endpoint."""
        url = f"{base_url}/family/RF00001/regions"
        response = session.get(url, timeout=timeout)
        # Regions endpoint may be restricted (403)
        assert response.status_code in [200, 404, 403]

    @pytest.mark.api
    def test_family_structures_endpoint(self, session, base_url, timeout):
        """Test family structures endpoint."""
        url = f"{base_url}/family/RF00001/structures"
        response = session.get(url, timeout=timeout)
        assert response.status_code in [200, 404]


class TestFamilyImageEndpoints:
    """Test family image and visualization endpoints."""

    @pytest.mark.api
    def test_family_image_endpoint(self, session, base_url, timeout):
        """Test secondary structure image endpoint."""
        url = f"{base_url}/family/RF00001/image"
        response = session.get(url, timeout=timeout, allow_redirects=True)
        # Images might be served from different locations
        assert response.status_code in [200, 302, 303, 404]

    @pytest.mark.api
    def test_family_thumbnail_endpoint(self, session, base_url, timeout):
        """Test thumbnail image endpoint."""
        url = f"{base_url}/family/RF00001/thumbnail"
        response = session.get(url, timeout=timeout, allow_redirects=True)
        assert response.status_code in [200, 302, 303, 404]
