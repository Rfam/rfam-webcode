"""
URL configuration for the Rfam API.
"""
from django.urls import path, re_path
from . import views

urlpatterns = [
    # Home
    path('', views.HomeView.as_view(), name='home'),

    # Submit alignment
    path('submit_alignment', views.submit_alignment, name='submit-alignment'),

    # Family endpoints
    path('family/<str:entry>', views.FamilyView.as_view(), name='family'),
    path('family/<str:entry>/alignment', views.FamilyAlignmentView.as_view(), name='family-alignment'),
    path('family/<str:entry>/tree', views.FamilyTreeView.as_view(), name='family-tree'),
    path('family/<str:entry>/tree/<str:subtype>', views.FamilyTreeView.as_view(), name='family-tree-subtype'),
    path('family/<str:entry>/cm', views.FamilyCMView.as_view(), name='family-cm'),
    path('family/<str:entry>/regions', views.FamilyRegionsView.as_view(), name='family-regions'),
    path('family/<str:entry>/refseq', views.FamilyRegionsView.as_view(), name='family-refseq'),
    path('family/<str:entry>/structures', views.FamilyStructuresView.as_view(), name='family-structures'),
    path('family/<str:entry>/thumbnail', views.FamilyThumbnailView.as_view(), name='family-thumbnail'),

    # Families browse
    path('families', views.FamiliesListView.as_view(), name='families'),
    path('families/', views.FamiliesListView.as_view(), name='families-slash'),
    path('families/<str:letter>', views.FamiliesListView.as_view(), name='families-letter'),
    path('families/with_structure', views.FamiliesWithStructureView.as_view(), name='families-with-structure'),
    path('families/top20', views.FamiliesTop20View.as_view(), name='families-top20'),

    # Clan endpoints
    path('clan/<str:entry>', views.ClanView.as_view(), name='clan'),
    path('clan/<str:entry>/structures', views.ClanStructuresView.as_view(), name='clan-structures'),

    # Clans browse
    path('clans', views.ClansListView.as_view(), name='clans'),
    path('clans/', views.ClansListView.as_view(), name='clans-slash'),

    # Motif endpoints
    path('motif/<str:entry>', views.MotifView.as_view(), name='motif'),

    # Motifs browse
    path('motifs', views.MotifsListView.as_view(), name='motifs'),
    path('motifs/', views.MotifsListView.as_view(), name='motifs-slash'),

    # Genome endpoints
    path('genome/<str:ncbi_id>', views.GenomeView.as_view(), name='genome'),
    path('genome/<str:ncbi_id>/gff/<str:auto_genome>', views.GenomeGFFView.as_view(), name='genome-gff'),

    # Genomes browse
    path('genomes', views.GenomesListView.as_view(), name='genomes'),
    path('genomes/', views.GenomesListView.as_view(), name='genomes-slash'),
    path('genomes/<str:kingdom>', views.GenomesListView.as_view(), name='genomes-kingdom'),

    # Sequence endpoints
    path('sequence', views.SequenceView.as_view(), name='sequence'),
    path('sequence/', views.SequenceView.as_view(), name='sequence-slash'),
    path('sequence/<str:accession>', views.SequenceView.as_view(), name='sequence-accession'),
    path('sequence/<str:accession>/hits', views.SequenceHitsView.as_view(), name='sequence-hits'),

    # Accession endpoint
    path('accession/<str:accession>', views.AccessionView.as_view(), name='accession'),

    # Structure endpoints
    path('structure/<str:pdb_id>', views.StructureView.as_view(), name='structure'),
    path('structure/<str:pdb_id>/av', views.StructureViewerView.as_view(), name='structure-viewer'),

    # Browse
    path('browse', views.BrowseIndexView.as_view(), name='browse'),
    path('browse/', views.BrowseIndexView.as_view(), name='browse-slash'),

    # Search endpoints
    path('search', views.SearchIndexView.as_view(), name='search'),
    path('search/', views.SearchIndexView.as_view(), name='search-slash'),
    path('search/keyword', views.KeywordSearchView.as_view(), name='search-keyword'),
    path('search/taxonomy', views.TaxonomySearchView.as_view(), name='search-taxonomy'),
    path('search/type', views.TypeSearchView.as_view(), name='search-type'),
    path('search/batch', views.BatchSearchView.as_view(), name='search-batch'),

    # Jump/smart search
    path('jump', views.JumpView.as_view(), name='jump'),

    # Help
    path('help', views.HelpView.as_view(), name='help'),
    path('help/', views.HelpView.as_view(), name='help-slash'),

    # Status
    path('status', views.StatusView.as_view(), name='status'),

    # Special pages
    path('covid-19', views.SpecialPageView.as_view(), {'page_name': 'covid-19'}, name='covid-19'),
    path('viruses', views.SpecialPageView.as_view(), {'page_name': 'viruses'}, name='viruses'),
    path('microrna', views.SpecialPageView.as_view(), {'page_name': 'microrna'}, name='microrna'),
    path('rfam20', views.SpecialPageView.as_view(), {'page_name': 'rfam20'}, name='rfam20'),
    path('3d', views.SpecialPageView.as_view(), {'page_name': '3d'}, name='3d'),

    # Articles
    path('articles', views.ArticlesView.as_view(), name='articles'),

    # Robots.txt
    path('robots.txt', views.RobotsTxtView.as_view(), name='robots'),
]
