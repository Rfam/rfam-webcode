"""
Custom renderers for Rfam API.
"""
from rest_framework.renderers import BaseRenderer
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom


class RfamXMLRenderer(BaseRenderer):
    """
    Renderer which serializes to XML in Rfam format.
    """
    media_type = 'text/xml'
    format = 'xml'
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into XML.
        """
        if data is None:
            return ''

        view = renderer_context.get('view') if renderer_context else None
        entity_type = getattr(view, 'entity_type', 'entry')

        # Create root element
        root = Element('rfam')
        root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        root.set('xmlns', 'https://rfam.org/')
        root.set('xsi:schemaLocation', 'https://rfam.org/ https://rfam.org/static/documents/schemas/entry.xsd')
        root.set('release', str(data.get('release', {}).get('number', '')))
        root.set('release_date', str(data.get('release', {}).get('date', '')))

        if entity_type == 'family':
            self._render_family(root, data)
        elif entity_type == 'clan':
            self._render_clan(root, data)
        elif entity_type == 'motif':
            self._render_motif(root, data)
        else:
            self._render_generic(root, data)

        # Generate XML string
        xml_string = tostring(root, encoding='unicode')
        # Pretty print
        try:
            dom = minidom.parseString(xml_string)
            return '<?xml version="1.0" encoding="UTF-8"?>\n' + dom.toprettyxml(indent="  ")[23:]  # Skip XML declaration from minidom
        except Exception:
            return '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_string

    def _render_family(self, root, data):
        """Render family data to XML."""
        rfam_data = data.get('rfam', data)

        entry = SubElement(root, 'entry')
        entry.set('entry_type', 'Rfam')
        entry.set('accession', str(rfam_data.get('acc', '')))
        entry.set('id', str(rfam_data.get('id', '')))

        # Description
        desc = SubElement(entry, 'description')
        desc.text = rfam_data.get('description', '')

        # Comment
        comment = SubElement(entry, 'comment')
        comment.text = rfam_data.get('comment', '')

        # Curation details
        curation = rfam_data.get('curation', {})
        curation_elem = SubElement(entry, 'curation_details')

        author = SubElement(curation_elem, 'author')
        author.text = str(curation.get('author', ''))

        seed_source = SubElement(curation_elem, 'seed_source')
        seed_source.text = str(curation.get('seed_source', ''))

        num_seqs = SubElement(curation_elem, 'num_seqs')
        seed = SubElement(num_seqs, 'seed')
        seed.text = str(curation.get('num_seed', 0))
        full = SubElement(num_seqs, 'full')
        full.text = str(curation.get('num_full', 0))

        num_species = SubElement(curation_elem, 'num_species')
        num_species.text = str(curation.get('num_species', 0))

        type_elem = SubElement(curation_elem, 'type')
        type_elem.text = str(curation.get('type', ''))

        structure_source = SubElement(curation_elem, 'structure_source')
        structure_source.text = str(curation.get('structure_source', ''))

        # CM details
        cm = rfam_data.get('cm', {})
        cm_elem = SubElement(entry, 'cm_details')

        build_cmd = SubElement(cm_elem, 'build_command')
        build_cmd.text = str(cm.get('build_command', ''))

        calibrate_cmd = SubElement(cm_elem, 'calibrate_command')
        calibrate_cmd.text = str(cm.get('calibrate_command', ''))

        search_cmd = SubElement(cm_elem, 'search_command')
        search_cmd.text = str(cm.get('search_command', ''))

        # Cutoffs
        cutoffs = cm.get('cutoffs', {})
        cutoffs_elem = SubElement(cm_elem, 'cutoffs')

        gathering = SubElement(cutoffs_elem, 'gathering')
        gathering.text = str(cutoffs.get('gathering', 0))

        trusted = SubElement(cutoffs_elem, 'trusted')
        trusted.text = str(cutoffs.get('trusted', 0))

        noise = SubElement(cutoffs_elem, 'noise')
        noise.text = str(cutoffs.get('noise', 0))

    def _render_clan(self, root, data):
        """Render clan data to XML."""
        entry = SubElement(root, 'entry')
        entry.set('entry_type', 'Clan')
        entry.set('accession', str(data.get('acc', '')))
        entry.set('id', str(data.get('id', '')))

        desc = SubElement(entry, 'description')
        desc.text = data.get('description', '')

        members = SubElement(entry, 'members')
        for member in data.get('members', []):
            member_elem = SubElement(members, 'member')
            member_elem.set('accession', member.get('acc', ''))
            member_elem.set('id', member.get('id', ''))

    def _render_motif(self, root, data):
        """Render motif data to XML."""
        entry = SubElement(root, 'entry')
        entry.set('entry_type', 'Motif')
        entry.set('accession', str(data.get('acc', '')))
        entry.set('id', str(data.get('id', '')))

        desc = SubElement(entry, 'description')
        desc.text = data.get('description', '')

    def _render_generic(self, root, data):
        """Render generic data to XML."""
        self._dict_to_xml(root, data)

    def _dict_to_xml(self, parent, data):
        """Convert a dictionary to XML elements."""
        if isinstance(data, dict):
            for key, value in data.items():
                child = SubElement(parent, str(key))
                self._dict_to_xml(child, value)
        elif isinstance(data, list):
            for item in data:
                child = SubElement(parent, 'item')
                self._dict_to_xml(child, item)
        else:
            parent.text = str(data) if data is not None else ''
