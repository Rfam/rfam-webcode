"""
Django models for the Rfam database.
These are unmanaged models that map to the existing Rfam MySQL database.
"""
from django.db import models


class DbVersion(models.Model):
    """Database version information."""
    rfam_release = models.FloatField(primary_key=True)
    rfam_release_date = models.DateTimeField()
    number_families = models.IntegerField()
    embl_release = models.TextField()
    genome_collection_date = models.DateTimeField(null=True, blank=True)
    refseq_version = models.IntegerField(null=True, blank=True)
    pdb_date = models.DateTimeField(null=True, blank=True)
    infernal_version = models.CharField(max_length=45, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'db_version'


class Family(models.Model):
    """Rfam family model."""
    rfam_acc = models.CharField(max_length=7, primary_key=True)
    rfam_id = models.CharField(max_length=40)
    auto_wiki = models.PositiveIntegerField()
    description = models.CharField(max_length=75, null=True, blank=True)
    author = models.TextField(null=True, blank=True)
    seed_source = models.TextField(null=True, blank=True)
    gathering_cutoff = models.FloatField(null=True, blank=True, db_column='gathering_cutoff')
    trusted_cutoff = models.FloatField(null=True, blank=True, db_column='trusted_cutoff')
    noise_cutoff = models.FloatField(null=True, blank=True, db_column='noise_cutoff')
    comment = models.TextField(null=True, blank=True)
    previous_id = models.TextField(null=True, blank=True)
    cmbuild = models.TextField(null=True, blank=True)
    cmcalibrate = models.TextField(null=True, blank=True)
    cmsearch = models.TextField(null=True, blank=True)
    num_seed = models.BigIntegerField(null=True, blank=True)
    num_full = models.BigIntegerField(null=True, blank=True)
    num_genome_seq = models.BigIntegerField(null=True, blank=True)
    num_refseq = models.BigIntegerField(null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True)
    structure_source = models.TextField(null=True, blank=True)
    number_of_species = models.BigIntegerField(null=True, blank=True)
    number_3d_structures = models.IntegerField(null=True, blank=True)
    num_pseudonokts = models.IntegerField(null=True, blank=True)
    tax_seed = models.TextField(null=True, blank=True)
    ecmli_lambda = models.FloatField(null=True, blank=True)
    ecmli_mu = models.FloatField(null=True, blank=True)
    ecmli_cal_db = models.IntegerField(null=True, blank=True)
    ecmli_cal_hits = models.IntegerField(null=True, blank=True)
    maxl = models.IntegerField(null=True, blank=True)
    clen = models.IntegerField(null=True, blank=True)
    match_pair_node = models.BooleanField(null=True, blank=True)
    hmm_tau = models.FloatField(null=True, blank=True)
    hmm_lambda = models.FloatField(null=True, blank=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'family'

    def __str__(self):
        return f"{self.rfam_acc} - {self.rfam_id}"


class Clan(models.Model):
    """Rfam clan model."""
    clan_acc = models.CharField(max_length=7, primary_key=True)
    id = models.CharField(max_length=40, null=True, blank=True)
    previous_id = models.TextField(null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    author = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created = models.DateTimeField()
    updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'clan'

    def __str__(self):
        return f"{self.clan_acc} - {self.id}"


class ClanMembership(models.Model):
    """Clan membership - links families to clans."""
    clan_acc = models.ForeignKey(
        Clan,
        on_delete=models.DO_NOTHING,
        db_column='clan_acc',
        related_name='memberships'
    )
    rfam_acc = models.OneToOneField(
        Family,
        on_delete=models.DO_NOTHING,
        db_column='rfam_acc',
        primary_key=True,
        related_name='clan_membership'
    )

    class Meta:
        managed = False
        db_table = 'clan_membership'


class Motif(models.Model):
    """Rfam motif model."""
    motif_acc = models.CharField(max_length=7, primary_key=True)
    motif_id = models.CharField(max_length=40, null=True, blank=True)
    description = models.CharField(max_length=75, null=True, blank=True)
    author = models.TextField(null=True, blank=True)
    seed_source = models.TextField(null=True, blank=True)
    gathering_cutoff = models.FloatField(null=True, blank=True)
    trusted_cutoff = models.FloatField(null=True, blank=True)
    noise_cutoff = models.FloatField(null=True, blank=True)
    cmbuild = models.TextField(null=True, blank=True)
    cmcalibrate = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True)
    num_seed = models.BigIntegerField(null=True, blank=True)
    average_id = models.FloatField(null=True, blank=True)
    average_sqlen = models.FloatField(null=True, blank=True)
    ecmli_lambda = models.FloatField(null=True, blank=True)
    ecmli_mu = models.FloatField(null=True, blank=True)
    ecmli_cal_db = models.IntegerField(null=True, blank=True)
    ecmli_cal_hits = models.IntegerField(null=True, blank=True)
    maxl = models.IntegerField(null=True, blank=True)
    clen = models.IntegerField(null=True, blank=True)
    match_pair_node = models.BooleanField(null=True, blank=True)
    hmm_tau = models.FloatField(null=True, blank=True)
    hmm_lambda = models.FloatField(null=True, blank=True)
    wiki = models.CharField(max_length=80, null=True, blank=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'motif'

    def __str__(self):
        return f"{self.motif_acc} - {self.motif_id}"


class Taxonomy(models.Model):
    """NCBI Taxonomy information."""
    ncbi_id = models.PositiveIntegerField(primary_key=True)
    species = models.CharField(max_length=100)
    tax_string = models.TextField(null=True, blank=True)
    tree_display_name = models.CharField(max_length=100, null=True, blank=True)
    align_display_name = models.CharField(max_length=112, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'taxonomy'

    def __str__(self):
        return f"{self.ncbi_id} - {self.species}"


class Genome(models.Model):
    """Genome information."""
    upid = models.CharField(max_length=20, primary_key=True)
    assembly_acc = models.CharField(max_length=20, null=True, blank=True)
    assembly_version = models.PositiveIntegerField(null=True, blank=True)
    wgs_acc = models.CharField(max_length=20, null=True, blank=True)
    wgs_version = models.PositiveIntegerField(null=True, blank=True)
    assembly_name = models.CharField(max_length=100, null=True, blank=True)
    assembly_level = models.CharField(max_length=20, null=True, blank=True)
    study_ref = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    total_length = models.BigIntegerField(null=True, blank=True)
    ungapped_length = models.BigIntegerField(null=True, blank=True)
    circular = models.SmallIntegerField(null=True, blank=True)
    ncbi_id = models.PositiveIntegerField()
    scientific_name = models.CharField(max_length=300, null=True, blank=True)
    common_name = models.CharField(max_length=200, null=True, blank=True)
    kingdom = models.CharField(max_length=50, null=True, blank=True)
    num_rfam_regions = models.IntegerField(null=True, blank=True)
    num_families = models.IntegerField(null=True, blank=True)
    is_reference = models.BooleanField(default=True)
    is_representative = models.BooleanField(default=False)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'genome'

    def __str__(self):
        return f"{self.upid} - {self.scientific_name}"


class FullRegion(models.Model):
    """Full region hit information for families."""
    rfam_acc = models.ForeignKey(
        Family,
        on_delete=models.DO_NOTHING,
        db_column='rfam_acc',
        related_name='full_regions'
    )
    rfamseq_acc = models.CharField(max_length=25)
    seq_start = models.BigIntegerField()
    seq_end = models.BigIntegerField()
    bit_score = models.FloatField()
    evalue_score = models.CharField(max_length=15)
    cm_start = models.PositiveIntegerField()
    cm_end = models.PositiveIntegerField()
    truncated = models.CharField(max_length=2)
    type = models.CharField(max_length=4)
    is_significant = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'full_region'


class SeedRegion(models.Model):
    """Seed region information for families."""
    rfam_acc = models.ForeignKey(
        Family,
        on_delete=models.DO_NOTHING,
        db_column='rfam_acc',
        related_name='seed_regions'
    )
    rfamseq_acc = models.CharField(max_length=25, null=True, blank=True)
    seq_start = models.BigIntegerField()
    seq_end = models.BigIntegerField()
    md5 = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'seed_region'


class Pdb(models.Model):
    """PDB structure information."""
    pdb_id = models.CharField(max_length=4, primary_key=True)
    keywords = models.TextField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    date = models.TextField(null=True, blank=True)
    resolution = models.FloatField(null=True, blank=True)
    method = models.TextField(null=True, blank=True)
    author = models.TextField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'pdb'

    def __str__(self):
        return self.pdb_id


class PdbFullRegion(models.Model):
    """PDB to family region mapping."""
    rfam_acc = models.CharField(max_length=7, primary_key=True)
    pdb_id = models.CharField(max_length=4)
    chain = models.CharField(max_length=4, null=True, blank=True)
    pdb_start = models.IntegerField()
    pdb_end = models.IntegerField()
    bit_score = models.FloatField()
    evalue_score = models.CharField(max_length=15)
    cm_start = models.IntegerField()
    cm_end = models.IntegerField()
    hex_colour = models.CharField(max_length=6, null=True, blank=True)
    is_significant = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'pdb_full_region'


class LiteratureReference(models.Model):
    """Literature reference."""
    pmid = models.IntegerField(primary_key=True)
    title = models.TextField(null=True, blank=True)
    author = models.TextField(null=True, blank=True)
    journal = models.TextField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'literature_reference'


class FamilyLiteratureReference(models.Model):
    """Family to literature reference mapping."""
    rfam_acc = models.ForeignKey(
        Family,
        on_delete=models.DO_NOTHING,
        db_column='rfam_acc',
        related_name='literature_references'
    )
    pmid = models.ForeignKey(
        LiteratureReference,
        on_delete=models.DO_NOTHING,
        db_column='pmid',
        related_name='families'
    )
    comment = models.TextField(null=True, blank=True)
    order_added = models.SmallIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'family_literature_reference'


class DatabaseLink(models.Model):
    """External database links for families."""
    rfam_acc = models.ForeignKey(
        Family,
        on_delete=models.DO_NOTHING,
        db_column='rfam_acc',
        related_name='database_links'
    )
    db_id = models.TextField()
    comment = models.TextField(null=True, blank=True)
    db_link = models.TextField()
    other_params = models.TextField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'database_link'
