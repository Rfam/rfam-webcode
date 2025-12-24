"""
Custom content negotiation for Rfam API.
Supports Accept header-based content negotiation and query parameter override.
"""
from rest_framework.negotiation import DefaultContentNegotiation


class RfamContentNegotiation(DefaultContentNegotiation):
    """
    Content negotiation that supports both Accept header and ?output= query parameter.
    """

    def select_renderer(self, request, renderers, format_suffix=None):
        """
        Select appropriate renderer based on Accept header or output parameter.
        """
        # Check for output query parameter
        output_format = request.query_params.get('output', '').lower()

        if output_format == 'xml':
            # Find XML renderer
            for renderer in renderers:
                if renderer.format == 'xml':
                    return (renderer, renderer.media_type)

        if output_format == 'json':
            # Find JSON renderer
            for renderer in renderers:
                if renderer.format == 'json':
                    return (renderer, renderer.media_type)

        # Fall back to default content negotiation (Accept header)
        return super().select_renderer(request, renderers, format_suffix)
