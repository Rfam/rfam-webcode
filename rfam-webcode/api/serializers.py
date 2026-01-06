"""
Serializers for Rfam API endpoints.
"""
from rest_framework import serializers
from .models import (
    Family, Clan, ClanMembership, Motif, Genome, Taxonomy,
    DbVersion, Pdb, PdbFullRegion
)


class DbVersionSerializer(serializers.ModelSerializer):
    """Serializer for database version information."""
    number = serializers.FloatField(source='rfam_release')
    date = serializers.DateTimeField(source='rfam_release_date', format='%Y-%m-%d')

    class Meta:
        model = DbVersion
        fields = ['number', 'date']


class CutoffsSerializer(serializers.Serializer):
    """Serializer for CM cutoffs."""
    gathering = serializers.FloatField()
    trusted = serializers.FloatField()
    noise = serializers.FloatField()


class CMSerializer(serializers.Serializer):
    """Serializer for covariance model details."""
    build_command = serializers.CharField()
    calibrate_command = serializers.CharField()
    search_command = serializers.CharField()
    cutoffs = CutoffsSerializer()


class CurationSerializer(serializers.Serializer):
    """Serializer for curation details."""
    author = serializers.CharField()
    seed_source = serializers.CharField()
    num_seed = serializers.IntegerField()
    num_full = serializers.IntegerField()
    num_species = serializers.IntegerField()
    type = serializers.CharField()
    structure_source = serializers.CharField()


class FamilyDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for family JSON response matching existing API format."""
    acc = serializers.CharField(source='rfam_acc')
    id = serializers.CharField(source='rfam_id')
    description = serializers.CharField()
    comment = serializers.CharField()

    curation = serializers.SerializerMethodField()
    cm = serializers.SerializerMethodField()
    release = serializers.SerializerMethodField()
    clan = serializers.SerializerMethodField()

    class Meta:
        model = Family
        fields = ['acc', 'id', 'description', 'comment', 'curation', 'cm', 'release', 'clan']

    def get_curation(self, obj):
        return {
            'author': obj.author or '',
            'seed_source': obj.seed_source or '',
            'num_seed': obj.num_seed or 0,
            'num_full': obj.num_full or 0,
            'num_species': obj.number_of_species or 0,
            'type': obj.type or '',
            'structure_source': obj.structure_source or '',
        }

    def get_cm(self, obj):
        return {
            'build_command': obj.cmbuild or '',
            'calibrate_command': obj.cmcalibrate or '',
            'search_command': obj.cmsearch or '',
            'cutoffs': {
                'gathering': obj.gathering_cutoff or 0.0,
                'trusted': obj.trusted_cutoff or 0.0,
                'noise': obj.noise_cutoff or 0.0,
            }
        }

    def get_release(self, obj):
        # Get the latest release info
        from .models import DbVersion
        try:
            version = DbVersion.objects.order_by('-rfam_release').first()
            if version:
                return {
                    'date': version.rfam_release_date.strftime('%Y-%m-%d') if version.rfam_release_date else '',
                    'number': f"{version.rfam_release:.2f}" if version.rfam_release else '0.00',
                }
        except Exception:
            pass
        return {'date': '', 'number': '0.00'}

    def get_clan(self, obj):
        # Get clan membership for this family
        from .models import ClanMembership
        try:
            membership = ClanMembership.objects.select_related('clan_acc').filter(
                rfam_acc=obj.rfam_acc
            ).first()
            if membership:
                return {
                    'acc': membership.clan_acc.clan_acc,
                    'id': membership.clan_acc.id,
                }
        except Exception:
            pass
        return {'acc': None, 'id': None}


class FamilyListSerializer(serializers.ModelSerializer):
    """Simplified serializer for family list views."""
    acc = serializers.CharField(source='rfam_acc')
    id = serializers.CharField(source='rfam_id')

    class Meta:
        model = Family
        fields = ['acc', 'id', 'description', 'type', 'num_seed', 'num_full']


class ClanDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for clan."""
    acc = serializers.CharField(source='clan_acc')
    members = serializers.SerializerMethodField()

    class Meta:
        model = Clan
        fields = ['acc', 'id', 'description', 'author', 'comment', 'members']

    def get_members(self, obj):
        memberships = ClanMembership.objects.filter(clan_acc=obj.clan_acc).select_related('rfam_acc')
        return [
            {
                'acc': m.rfam_acc.rfam_acc,
                'id': m.rfam_acc.rfam_id,
                'description': m.rfam_acc.description,
            }
            for m in memberships
        ]


class ClanListSerializer(serializers.ModelSerializer):
    """Simplified serializer for clan list views."""
    acc = serializers.CharField(source='clan_acc')

    class Meta:
        model = Clan
        fields = ['acc', 'id', 'description']


class MotifDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for motif."""
    acc = serializers.CharField(source='motif_acc')
    id = serializers.CharField(source='motif_id')

    class Meta:
        model = Motif
        fields = ['acc', 'id', 'description', 'author', 'type', 'num_seed']


class MotifListSerializer(serializers.ModelSerializer):
    """Simplified serializer for motif list views."""
    acc = serializers.CharField(source='motif_acc')
    id = serializers.CharField(source='motif_id')

    class Meta:
        model = Motif
        fields = ['acc', 'id', 'description']


class GenomeDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for genome."""

    class Meta:
        model = Genome
        fields = [
            'upid', 'ncbi_id', 'scientific_name', 'common_name', 'kingdom',
            'assembly_acc', 'assembly_name', 'assembly_level',
            'total_length', 'num_rfam_regions', 'num_families'
        ]


class GenomeListSerializer(serializers.ModelSerializer):
    """Simplified serializer for genome list views."""

    class Meta:
        model = Genome
        fields = ['upid', 'ncbi_id', 'scientific_name', 'kingdom', 'num_rfam_regions']


class TaxonomySerializer(serializers.ModelSerializer):
    """Serializer for taxonomy information."""

    class Meta:
        model = Taxonomy
        fields = ['ncbi_id', 'species', 'tax_string']


class PdbSerializer(serializers.ModelSerializer):
    """Serializer for PDB structures."""

    class Meta:
        model = Pdb
        fields = ['pdb_id', 'title', 'method', 'resolution']
