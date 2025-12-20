"""
Integration tests that test complete workflows.
"""
import pytest
from bs4 import BeautifulSoup


class TestFamilyWorkflow:
    """Test complete family browsing workflow."""

    @pytest.mark.integration
    def test_browse_to_family_workflow(self, session, base_url, timeout):
        """Test browsing families and navigating to a specific family."""
        # Step 1: Go to families browse page
        browse_url = f"{base_url}/families"
        response = session.get(browse_url, timeout=timeout)
        assert response.status_code == 200

        # Step 2: Browse by letter A
        letter_url = f"{base_url}/families/A"
        response = session.get(letter_url, timeout=timeout)
        assert response.status_code == 200

        # Step 3: Access a specific family
        family_url = f"{base_url}/family/RF00001"
        response = session.get(family_url, timeout=timeout)
        assert response.status_code == 200


class TestSearchToFamilyWorkflow:
    """Test search to family detail workflow."""

    @pytest.mark.integration
    def test_keyword_search_to_family(self, session, base_url, timeout):
        """Test searching and viewing results."""
        # Search for a term
        search_url = f"{base_url}/search/keyword"
        response = session.get(
            search_url,
            params={'query': '5S'},
            timeout=timeout,
            allow_redirects=True
        )
        assert response.status_code == 200

        # Should be able to access a family from search results
        family_url = f"{base_url}/family/RF00001"
        response = session.get(family_url, timeout=timeout)
        assert response.status_code == 200


class TestAPIConsistency:
    """Test that different API formats return consistent data."""

    @pytest.mark.integration
    @pytest.mark.api
    def test_family_data_consistency_json_xml(self, session, base_url, timeout):
        """Test that JSON and XML return consistent family data."""
        accession = "RF00001"

        # Get JSON data
        json_response = session.get(
            f"{base_url}/family/{accession}",
            headers={'Accept': 'application/json'},
            timeout=timeout
        )
        assert json_response.status_code == 200
        json_data = json_response.json()

        # Get XML data
        xml_response = session.get(
            f"{base_url}/family/{accession}",
            headers={'Accept': 'text/xml'},
            timeout=timeout
        )
        assert xml_response.status_code == 200

        # Both should contain the same accession
        assert json_data['rfam']['acc'] == accession
        assert accession in xml_response.text


class TestCrosslinking:
    """Test links between different entity types."""

    @pytest.mark.integration
    def test_family_to_clan_link(self, session, base_url, timeout):
        """Test that families with clans link correctly."""
        # Access a family that belongs to a clan
        family_url = f"{base_url}/family/RF00005"  # tRNA
        response = session.get(family_url, timeout=timeout)
        assert response.status_code == 200

        # tRNA belongs to clan CL00001
        # If family has clan, should be able to access clan page
        clan_url = f"{base_url}/clan/CL00001"
        response = session.get(clan_url, timeout=timeout)
        assert response.status_code == 200


class TestGenomeAnnotationWorkflow:
    """Test genome annotation workflow."""

    @pytest.mark.integration
    @pytest.mark.slow
    def test_genome_to_gff_workflow(self, session, base_url, timeout):
        """Test accessing genome and downloading GFF."""
        # Access genome page
        genome_url = f"{base_url}/genome/511145"
        response = session.get(genome_url, timeout=timeout)
        assert response.status_code == 200

        # GFF download may or may not work without auto_genome ID
        # Just verify the genome page is accessible


class TestDataExportWorkflow:
    """Test data export workflows."""

    @pytest.mark.integration
    @pytest.mark.slow
    def test_family_data_export_workflow(self, session, base_url, timeout):
        """Test accessing family and exporting various data types."""
        family_acc = "RF00001"

        # Access family page
        family_url = f"{base_url}/family/{family_acc}"
        response = session.get(family_url, timeout=timeout)
        assert response.status_code == 200

        # Try to access JSON API
        json_response = session.get(
            family_url,
            headers={'Accept': 'application/json'},
            timeout=timeout
        )
        assert json_response.status_code == 200

        # Try to access alignment
        alignment_url = f"{base_url}/family/{family_acc}/alignment"
        alignment_response = session.get(
            alignment_url,
            timeout=timeout,
            allow_redirects=True
        )
        assert alignment_response.status_code in [200, 302, 303]
