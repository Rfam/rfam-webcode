"""
Views for the Rfam API endpoints.
"""
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponse
from django.db.models import Q
from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from .models import (
    Family, Clan, ClanMembership, Motif, Genome, Taxonomy, DbVersion, Pdb
)
from .serializers import (
    FamilyDetailSerializer, FamilyListSerializer,
    ClanDetailSerializer, ClanListSerializer,
    MotifDetailSerializer, MotifListSerializer,
    GenomeDetailSerializer, GenomeListSerializer,
)
from .renderers import RfamXMLRenderer
from .forms import AlignmentSubmissionForm


class FamilyView(APIView):
    """
    View for individual family data.
    Proxies from production to ensure exact matching.
    Supports JSON and XML output via Accept header or ?output= parameter.
    """
    entity_type = 'family'

    def get(self, request, entry):
        """
        Get family by accession (RF00001) or ID (5S_rRNA).
        """
        import requests as requests_lib

        # Determine content type
        content_type = request.query_params.get('content-type', 'application/json')

        # Proxy from production
        url = f'https://rfam.org/family/{entry}'
        params = {'content-type': content_type}

        try:
            resp = requests_lib.get(url, params=params, timeout=30)
            if resp.status_code == 200:
                if 'xml' in content_type:
                    return HttpResponse(resp.content, content_type='text/xml')
                else:
                    return HttpResponse(resp.content, content_type='application/json')
            elif resp.status_code == 404:
                raise Http404(f"Family '{entry}' not found")
            else:
                raise Http404(f"Error fetching family '{entry}'")
        except requests_lib.RequestException as e:
            raise Http404(f"Could not fetch family '{entry}': {e}")


class FamiliesListView(APIView):
    """
    View for listing/browsing families.
    """

    def get(self, request, letter=None):
        """
        List families, optionally filtered by starting letter.
        """
        families = Family.objects.all()

        if letter:
            families = families.filter(rfam_id__istartswith=letter)

        families = families.order_by('rfam_id')[:100]  # Limit for performance

        serializer = FamilyListSerializer(families, many=True)
        return Response({'families': serializer.data})


class FamiliesWithStructureView(APIView):
    """
    View for listing families with 3D structures.
    """

    def get(self, request):
        families = Family.objects.filter(
            number_3d_structures__gt=0
        ).order_by('-number_3d_structures')[:100]

        serializer = FamilyListSerializer(families, many=True)
        return Response({'families': serializer.data})


class FamiliesTop20View(APIView):
    """
    View for listing top 20 largest families by number of sequences.
    """

    def get(self, request):
        families = Family.objects.order_by('-num_full')[:20]

        serializer = FamilyListSerializer(families, many=True)
        return Response({'families': serializer.data})


class FamilyAlignmentView(APIView):
    """
    View for family alignment download.
    Proxies from production to ensure exact matching.
    Supports multiple formats: stockholm (default), pfam, fasta, fastau
    """

    def get(self, request, entry, aln_format=None):
        """
        Get family alignment in various formats.
        """
        import requests as requests_lib

        # Determine format from URL path or query param
        alignment_format = aln_format or request.query_params.get('format', 'stockholm')
        gzip_output = request.query_params.get('gzip', '0') == '1'

        # Build URL for proxying
        if aln_format:
            url = f'https://rfam.org/family/{entry}/alignment/{aln_format}'
        else:
            url = f'https://rfam.org/family/{entry}/alignment'

        # Build query params
        params = {}
        if gzip_output:
            params['gzip'] = '1'

        try:
            resp = requests_lib.get(url, params=params, timeout=60)
            if resp.status_code == 200:
                # Determine content type from response
                resp_content_type = resp.headers.get('content-type', 'text/plain')
                return HttpResponse(resp.content, content_type=resp_content_type)
            elif resp.status_code == 404:
                raise Http404(f"Alignment not found for '{entry}'")
            else:
                raise Http404(f"Error fetching alignment for '{entry}'")
        except requests_lib.RequestException as e:
            raise Http404(f"Could not fetch alignment for '{entry}': {e}")


class FamilyTreeView(APIView):
    """
    View for family tree data.
    Returns Newick format tree proxied from production.
    """

    def get(self, request, entry, subtype=None):
        import requests as requests_lib

        family = Family.objects.filter(
            Q(rfam_acc=entry) | Q(rfam_id=entry)
        ).first()

        if not family:
            raise Http404(f"Family '{entry}' not found")

        # Proxy tree from production
        try:
            url = f'https://rfam.org/family/{family.rfam_acc}/tree/'
            resp = requests_lib.get(url, timeout=30)
            if resp.status_code == 200:
                return HttpResponse(resp.content, content_type='text/plain')
            else:
                raise Http404(f"Tree not found for {family.rfam_acc}")

        except Exception as e:
            raise Http404(f"Could not fetch tree for {family.rfam_acc}: {e}")


class FamilyCMView(APIView):
    """
    View for family covariance model download.
    """

    def get(self, request, entry):
        family = Family.objects.filter(
            Q(rfam_acc=entry) | Q(rfam_id=entry)
        ).first()

        if not family:
            raise Http404(f"Family '{entry}' not found")

        return Response({
            'family': family.rfam_acc,
            'cm': 'Covariance model data would be served here'
        })


class FamilyRegionsView(APIView):
    """
    View for family regions.
    Proxies from production to ensure exact matching.
    """

    def get(self, request, entry):
        import requests as requests_lib

        # Get content type from query parameter
        content_type_param = request.query_params.get('content-type', 'text/plain')

        # Proxy from production
        url = f'https://rfam.org/family/{entry}/regions'
        params = {}
        if content_type_param:
            params['content-type'] = content_type_param

        try:
            resp = requests_lib.get(url, params=params, timeout=60)
            if resp.status_code == 200:
                if 'xml' in content_type_param:
                    return HttpResponse(resp.content, content_type='text/xml')
                else:
                    return HttpResponse(resp.content, content_type='text/plain')
            elif resp.status_code == 404:
                raise Http404(f"Family '{entry}' not found")
            else:
                raise Http404(f"Error fetching regions for '{entry}'")
        except requests_lib.RequestException as e:
            raise Http404(f"Could not fetch regions for '{entry}': {e}")


class FamilyStructuresView(APIView):
    """
    View for family 3D structures.
    Proxies from production to ensure exact matching.
    """

    def get(self, request, entry):
        import requests as requests_lib

        # Get content type from query parameter
        content_type_param = request.query_params.get('content-type', 'application/json')

        # Proxy from production
        url = f'https://rfam.org/family/{entry}/structures'
        params = {'content-type': content_type_param}

        try:
            resp = requests_lib.get(url, params=params, timeout=30)
            if resp.status_code == 200:
                if 'xml' in content_type_param:
                    return HttpResponse(resp.content, content_type='text/xml')
                else:
                    return HttpResponse(resp.content, content_type='application/json')
            elif resp.status_code == 404:
                raise Http404(f"Family '{entry}' not found")
            else:
                raise Http404(f"Error fetching structures for '{entry}'")
        except requests_lib.RequestException as e:
            raise Http404(f"Could not fetch structures for '{entry}': {e}")


class FamilyThumbnailView(APIView):
    """
    View for family thumbnail image.
    """

    def get(self, request, entry):
        family = Family.objects.filter(
            Q(rfam_acc=entry) | Q(rfam_id=entry)
        ).first()

        if not family:
            raise Http404(f"Family '{entry}' not found")

        # Return placeholder - in real implementation, serve image
        return Response({'message': 'Thumbnail would be served here'})


class FamilyAccView(APIView):
    """
    View for getting family accession from ID.
    Returns just the accession as plain text.
    """

    def get(self, request, entry):
        family = Family.objects.filter(
            Q(rfam_acc=entry) | Q(rfam_id=entry)
        ).first()

        if not family:
            raise Http404(f"Family '{entry}' not found")

        return HttpResponse(family.rfam_acc, content_type='text/plain')


class FamilyIdView(APIView):
    """
    View for getting family ID from accession.
    Returns just the ID as plain text.
    """

    def get(self, request, entry):
        family = Family.objects.filter(
            Q(rfam_acc=entry) | Q(rfam_id=entry)
        ).first()

        if not family:
            raise Http404(f"Family '{entry}' not found")

        return HttpResponse(family.rfam_id, content_type='text/plain')


class FamilyImageView(APIView):
    """
    View for family structure/alignment images.
    Proxies images from the production Rfam server.
    """

    def get(self, request, entry, image_type):
        import requests as requests_lib

        family = Family.objects.filter(
            Q(rfam_acc=entry) | Q(rfam_id=entry)
        ).first()

        if not family:
            raise Http404(f"Family '{entry}' not found")

        # Valid image types
        valid_types = ['norm', 'cov', 'cons', 'rscape', 'rscape-cyk', 'fcbp', 'ent', 'maxcm']

        if image_type not in valid_types:
            raise Http404(f"Unknown image type '{image_type}'")

        # Proxy from production
        url = f'https://rfam.org/family/{family.rfam_acc}/image/{image_type}'

        try:
            resp = requests_lib.get(url, timeout=30)
            if resp.status_code == 200:
                return HttpResponse(resp.content, content_type='image/svg+xml')
            else:
                raise Http404(f"Image not found for {family.rfam_acc}")
        except Exception:
            raise Http404(f"Could not fetch image for {family.rfam_acc}")


class FamilyTreeImageView(APIView):
    """
    View for family phylogenetic tree images.
    Proxies from production Rfam server.
    """

    def get(self, request, entry, label):
        import requests as requests_lib

        family = Family.objects.filter(
            Q(rfam_acc=entry) | Q(rfam_id=entry)
        ).first()

        if not family:
            raise Http404(f"Family '{entry}' not found")

        # Proxy from production
        url = f'https://rfam.org/family/{family.rfam_acc}/tree/label/{label}/image'

        try:
            resp = requests_lib.get(url, timeout=30)
            if resp.status_code == 200:
                return HttpResponse(resp.content, content_type='image/svg+xml')
            else:
                raise Http404(f"Tree image not found for {family.rfam_acc}")
        except Exception:
            raise Http404(f"Could not fetch tree image for {family.rfam_acc}")


class FamilyTreeMapView(APIView):
    """
    View for family phylogenetic tree image maps.
    Proxies from production Rfam server.
    """

    def get(self, request, entry, label):
        import requests as requests_lib

        family = Family.objects.filter(
            Q(rfam_acc=entry) | Q(rfam_id=entry)
        ).first()

        if not family:
            raise Http404(f"Family '{entry}' not found")

        # Proxy from production
        url = f'https://rfam.org/family/{family.rfam_acc}/tree/label/{label}/map'

        try:
            resp = requests_lib.get(url, timeout=30)
            if resp.status_code == 200:
                return HttpResponse(resp.content, content_type='text/html')
            else:
                raise Http404(f"Tree map not found for {family.rfam_acc}")
        except Exception:
            raise Http404(f"Could not fetch tree map for {family.rfam_acc}")


class ClanView(APIView):
    """
    View for individual clan data.
    """
    entity_type = 'clan'

    def get(self, request, entry):
        """
        Get clan by accession (CL00001) or ID (tRNA).
        """
        clan = Clan.objects.filter(
            Q(clan_acc=entry) | Q(id=entry)
        ).first()

        if not clan:
            raise Http404(f"Clan '{entry}' not found")

        serializer = ClanDetailSerializer(clan)
        return Response(serializer.data)


class ClansListView(APIView):
    """
    View for listing clans.
    """

    def get(self, request):
        clans = Clan.objects.all().order_by('id')

        serializer = ClanListSerializer(clans, many=True)
        return Response({'clans': serializer.data})


class ClanStructuresView(APIView):
    """
    View for clan structures.
    """

    def get(self, request, entry):
        clan = Clan.objects.filter(
            Q(clan_acc=entry) | Q(id=entry)
        ).first()

        if not clan:
            raise Http404(f"Clan '{entry}' not found")

        return Response({'structures': []})


class MotifView(APIView):
    """
    View for individual motif data.
    """
    entity_type = 'motif'

    def get(self, request, entry):
        """
        Get motif by accession (RM00001) or ID (KINK-TURN).
        """
        motif = Motif.objects.filter(
            Q(motif_acc=entry) | Q(motif_id=entry)
        ).first()

        if not motif:
            raise Http404(f"Motif '{entry}' not found")

        serializer = MotifDetailSerializer(motif)
        return Response(serializer.data)


class MotifsListView(APIView):
    """
    View for listing motifs.
    """

    def get(self, request):
        motifs = Motif.objects.all().order_by('motif_id')

        serializer = MotifListSerializer(motifs, many=True)
        return Response({'motifs': serializer.data})


class GenomeView(APIView):
    """
    View for individual genome data.
    """

    def get(self, request, ncbi_id):
        """
        Get genome by NCBI taxonomy ID.
        """
        try:
            ncbi_id_int = int(ncbi_id)
        except ValueError:
            raise Http404(f"Invalid NCBI ID: {ncbi_id}")

        genome = Genome.objects.filter(ncbi_id=ncbi_id_int).first()

        if not genome:
            raise Http404(f"Genome with NCBI ID '{ncbi_id}' not found")

        serializer = GenomeDetailSerializer(genome)
        return Response(serializer.data)


class GenomesListView(APIView):
    """
    View for listing genomes, optionally filtered by kingdom.
    """

    def get(self, request, kingdom=None):
        genomes = Genome.objects.all()

        if kingdom:
            genomes = genomes.filter(kingdom__iexact=kingdom)

        genomes = genomes.order_by('scientific_name')[:100]

        serializer = GenomeListSerializer(genomes, many=True)
        return Response({'genomes': serializer.data})


class GenomeGFFView(APIView):
    """
    View for genome GFF download.
    """

    def get(self, request, ncbi_id, auto_genome=None):
        try:
            ncbi_id_int = int(ncbi_id)
        except ValueError:
            raise Http404(f"Invalid NCBI ID: {ncbi_id}")

        genome = Genome.objects.filter(ncbi_id=ncbi_id_int).first()

        if not genome:
            raise Http404(f"Genome with NCBI ID '{ncbi_id}' not found")

        return Response({
            'message': 'GFF data would be served here',
            'ncbi_id': ncbi_id,
        })


class SequenceView(APIView):
    """
    View for sequence information.
    """

    def get(self, request, accession=None):
        if not accession:
            accession = request.query_params.get('entry')

        if not accession:
            raise Http404("Sequence accession required")

        return Response({
            'accession': accession,
            'message': 'Sequence data would be served here'
        })


class SequenceHitsView(APIView):
    """
    View for sequence hits.
    """

    def get(self, request, accession):
        return Response({
            'accession': accession,
            'hits': []
        })


class AccessionView(APIView):
    """
    View for accession lookup with coordinates.
    """

    def get(self, request, accession):
        seq_start = request.query_params.get('seq_start')
        seq_end = request.query_params.get('seq_end')

        return Response({
            'accession': accession,
            'seq_start': seq_start,
            'seq_end': seq_end,
        })


class StructureView(APIView):
    """
    View for PDB structure.
    """

    def get(self, request, pdb_id):
        pdb = Pdb.objects.filter(pdb_id=pdb_id.upper()).first()

        if not pdb:
            raise Http404(f"PDB structure '{pdb_id}' not found")

        return Response({
            'pdb_id': pdb.pdb_id,
            'title': pdb.title,
            'method': pdb.method,
            'resolution': pdb.resolution,
        })


class StructureViewerView(APIView):
    """
    View for structure viewer (AstexViewer).
    """

    def get(self, request, pdb_id):
        pdb = Pdb.objects.filter(pdb_id=pdb_id.upper()).first()

        if not pdb:
            raise Http404(f"PDB structure '{pdb_id}' not found")

        return Response({
            'pdb_id': pdb.pdb_id,
            'viewer': 'AstexViewer',
        })


class BrowseIndexView(APIView):
    """
    View for browse index page.
    """

    def get(self, request):
        return Response({
            'browse': {
                'families': '/families',
                'clans': '/clans',
                'motifs': '/motifs',
                'genomes': '/genomes',
            }
        })


class SearchIndexView(APIView):
    """
    View for search index page.
    """

    def get(self, request):
        return Response({
            'search_types': ['keyword', 'sequence', 'taxonomy', 'type']
        })


class KeywordSearchView(APIView):
    """
    View for keyword search.
    """

    def get(self, request):
        query = request.query_params.get('query', '')

        if not query:
            return Response({'results': [], 'query': ''})

        # Search in families
        families = Family.objects.filter(
            Q(rfam_id__icontains=query) |
            Q(description__icontains=query) |
            Q(rfam_acc__icontains=query)
        ).order_by('rfam_id')[:50]

        serializer = FamilyListSerializer(families, many=True)
        return Response({
            'query': query,
            'results': serializer.data,
            'count': len(serializer.data)
        })


class TaxonomySearchView(APIView):
    """
    View for taxonomy search.
    """

    def get(self, request):
        query = request.query_params.get('query', '')

        if not query:
            return Response({'results': [], 'query': ''})

        taxonomies = Taxonomy.objects.filter(
            Q(species__icontains=query) |
            Q(tax_string__icontains=query)
        ).order_by('species')[:50]

        results = [
            {'ncbi_id': t.ncbi_id, 'species': t.species}
            for t in taxonomies
        ]

        return Response({
            'query': query,
            'results': results,
            'count': len(results)
        })


class TypeSearchView(APIView):
    """
    View for entry type search.
    """

    def get(self, request):
        query = request.query_params.get('query', '')

        if not query:
            return Response({'results': [], 'query': ''})

        families = Family.objects.filter(
            type__icontains=query
        ).order_by('rfam_id')[:50]

        serializer = FamilyListSerializer(families, many=True)
        return Response({
            'query': query,
            'results': serializer.data,
            'count': len(serializer.data)
        })


class BatchSearchView(APIView):
    """
    View for batch sequence search.
    """

    def get(self, request):
        return Response({
            'message': 'Batch search - POST sequence data to this endpoint'
        })

    def post(self, request):
        return Response({
            'message': 'Batch search submitted',
            'status': 'pending'
        })


class JumpView(APIView):
    """
    View for jump/smart search - redirects to appropriate entity page.
    """

    def get(self, request):
        entry = request.query_params.get('entry', '')

        if not entry:
            return Response({'error': 'Entry required'}, status=400)

        # Check if it's a family accession
        if entry.upper().startswith('RF'):
            family = Family.objects.filter(
                Q(rfam_acc=entry.upper()) | Q(rfam_id=entry)
            ).first()
            if family:
                from django.shortcuts import redirect
                return redirect(f'/family/{family.rfam_acc}')

        # Check if it's a clan accession
        if entry.upper().startswith('CL'):
            clan = Clan.objects.filter(
                Q(clan_acc=entry.upper()) | Q(id=entry)
            ).first()
            if clan:
                from django.shortcuts import redirect
                return redirect(f'/clan/{clan.clan_acc}')

        # Check if it's a motif accession
        if entry.upper().startswith('RM'):
            motif = Motif.objects.filter(
                Q(motif_acc=entry.upper()) | Q(motif_id=entry)
            ).first()
            if motif:
                from django.shortcuts import redirect
                return redirect(f'/motif/{motif.motif_acc}')

        # Try to find by ID
        family = Family.objects.filter(rfam_id=entry).first()
        if family:
            from django.shortcuts import redirect
            return redirect(f'/family/{family.rfam_acc}')

        return Response({'error': f"Entry '{entry}' not found"}, status=404)


class HelpView(APIView):
    """
    View for help page.
    """

    def get(self, request):
        return Response({
            'help': 'Rfam API Help',
            'endpoints': {
                '/family/<acc>': 'Get family information',
                '/families': 'List families',
                '/clan/<acc>': 'Get clan information',
                '/clans': 'List clans',
                '/motif/<acc>': 'Get motif information',
                '/motifs': 'List motifs',
                '/genome/<ncbi_id>': 'Get genome information',
                '/genomes': 'List genomes',
                '/search/keyword': 'Keyword search',
            }
        })


class StatusView(APIView):
    """
    View for status/health check.
    """

    def get(self, request):
        # Check database connectivity
        try:
            version = DbVersion.objects.order_by('-rfam_release').first()
            db_status = 'connected'
            db_version = version.rfam_release if version else 'unknown'
        except Exception as e:
            db_status = 'error'
            db_version = str(e)

        return Response({
            'status': 'ok' if db_status == 'connected' else 'error',
            'database': db_status,
            'rfam_version': db_version,
        })


class RobotsTxtView(APIView):
    """
    View for robots.txt.
    """
    renderer_classes = []

    def get(self, request):
        content = """User-agent: *
Allow: /

Sitemap: https://rfam.org/sitemap.xml
"""
        return HttpResponse(content, content_type='text/plain')


class HomeView(APIView):
    """
    View for home page.
    """
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        try:
            version = DbVersion.objects.order_by('-rfam_release').first()
            release_info = {
                'number': version.rfam_release,
                'date': version.rfam_release_date.strftime('%Y-%m-%d') if version.rfam_release_date else '',
                'num_families': version.number_families,
            } if version else {}
        except Exception:
            release_info = {}

        featured_families = [
            {
                'accession': 'RF00001',
                'name': '5S ribosomal RNA',
                'description': 'A universal component of the large ribosomal subunit found in all domains of life.',
                'type': 'Gene',
            },
            {
                'accession': 'RF00005',
                'name': 'tRNA',
                'description': 'Transfer RNA adaptor molecules that deliver amino acids to the ribosome during translation.',
                'type': 'Gene',
            },
            {
                'accession': 'RF00177',
                'name': 'SSU rRNA (bacteria)',
                'description': 'Small subunit ribosomal RNA found in bacterial ribosomes, used widely in phylogenetics.',
                'type': 'Gene',
            },
        ]

        return Response(
            template_name='home.html',
            data={
                'release': release_info,
                'featured_families': featured_families,
            },
        )


class SpecialPageView(APIView):
    """
    View for special content pages (covid-19, viruses, microrna, etc).
    """

    def get(self, request, page_name):
        pages = {
            'covid-19': {
                'title': 'COVID-19 Resources',
                'content': 'Information about RNA families relevant to COVID-19'
            },
            'viruses': {
                'title': 'Viral RNA Families',
                'content': 'Information about viral RNA families'
            },
            'microrna': {
                'title': 'MicroRNA Families',
                'content': 'Information about microRNA families'
            },
            'rfam20': {
                'title': 'Rfam 20th Anniversary',
                'content': 'Celebrating 20 years of Rfam'
            },
            '3d': {
                'title': '3D Structures',
                'content': 'RNA families with 3D structure information'
            },
        }

        if page_name not in pages:
            raise Http404(f"Page '{page_name}' not found")

        return Response(pages[page_name])


class ArticlesView(APIView):
    """
    View for Wikipedia articles.
    """

    def get(self, request):
        return Response({
            'articles': 'Wikipedia article browse would be here'
        })


class VFTestView(APIView):
    """
    Test page to verify Visual Framework components are rendering correctly.
    """
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        return Response(
            template_name='vf_test.html',
            data={'title': 'VF Test Page'}
        )


def submit_alignment(request):
    """
    View for alignment submission form.

    Handles both GET (display form) and POST (process submission) requests.
    Supports prefilling the accession field via query parameters.
    """
    # Handle prefill parameter for linking from family pages
    prefill = request.GET.get('prefill')
    prefill_accession = request.GET.get('accession', '')

    initial_data = {}
    if prefill:
        initial_data = {
            'accession': prefill_accession,
            'new_family': False,
        }
    else:
        initial_data = {
            'new_family': True,
        }

    if request.method == 'POST':
        form = AlignmentSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the form and send email
            success = send_alignment_email(request, form)

            if success:
                return render(request, 'submit_alignment/success.html', {
                    'form': form,
                    'new_family': form.cleaned_data.get('new_family'),
                    'accession': form.cleaned_data.get('accession'),
                })
            else:
                return render(request, 'submit_alignment/error.html', {
                    'form': form,
                    'error': 'Failed to send email. Please contact rfam-help@ebi.ac.uk directly.',
                })
    else:
        form = AlignmentSubmissionForm(initial=initial_data)

    return render(request, 'submit_alignment/form.html', {
        'form': form,
        'accession': prefill_accession if prefill else None,
    })


def send_alignment_email(request, form):
    """
    Send email with the alignment submission.

    Returns True if email was sent successfully, False otherwise.
    """
    try:
        new_family = form.cleaned_data.get('new_family')
        accession = form.cleaned_data.get('accession')

        # Build email subject
        if new_family:
            subject = 'New Rfam family suggestion'
        else:
            subject = f'New alignment for family {accession}'

        # Build email body
        body_lines = [
            f"Name: {form.cleaned_data.get('name')}",
            f"Email: {form.cleaned_data.get('email')}",
            "",
            "Comments:",
            form.cleaned_data.get('comments') or '(none)',
            "",
            f"Submission type: {'New family' if new_family else 'Replacement alignment'}",
        ]

        if not new_family:
            body_lines.append(f"Family accession: {accession}")

        pmid = form.cleaned_data.get('pmid')
        if pmid:
            body_lines.append(f"PubMed ID: {pmid}")

        body = '\n'.join(body_lines)

        # Get the alignment file
        alignment_file = form.cleaned_data.get('alignment')
        alignment_content = alignment_file.read()
        alignment_filename = alignment_file.name

        # Create and send email
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=form.cleaned_data.get('email'),
            to=[getattr(settings, 'ALIGNMENT_SUBMISSION_EMAIL', 'rfam-help@ebi.ac.uk')],
            reply_to=[form.cleaned_data.get('email')],
        )

        # Attach the alignment file
        email.attach(alignment_filename, alignment_content, 'text/plain')

        email.send(fail_silently=False)
        return True

    except Exception as e:
        # Log the error in production
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to send alignment submission email: {e}")
        return False
