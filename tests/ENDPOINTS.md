# Rfam Website Endpoints Reference

This document catalogs all endpoints tested in the test suite, organized by functionality.

## Table of Contents

- [Family Endpoints](#family-endpoints)
- [Clan Endpoints](#clan-endpoints)
- [Genome Endpoints](#genome-endpoints)
- [Motif Endpoints](#motif-endpoints)
- [Browse Endpoints](#browse-endpoints)
- [Search Endpoints](#search-endpoints)
- [Sequence Endpoints](#sequence-endpoints)
- [Structure Endpoints](#structure-endpoints)
- [Tree and Visualization Endpoints](#tree-and-visualization-endpoints)
- [Static Pages](#static-pages)
- [API Formats](#api-formats)

---

## Family Endpoints

### Main Family Page
- **URL**: `/family/{acc_or_id}`
- **Methods**: GET
- **Formats**: HTML, JSON, XML
- **Examples**:
  - `/family/RF00001` - By accession
  - `/family/5S_rRNA` - By ID
- **Tests**: `test_family.py`

### Family Data Endpoints

#### Alignment
- **URL**: `/family/{acc}/alignment`
- **Parameters**: `?format={stockholm|pfam|fasta|clustal|phylip|psiblast}`
- **Methods**: GET
- **Examples**:
  - `/family/RF00001/alignment`
  - `/family/RF00001/alignment?format=fasta`
- **Tests**: `test_alignment_formats.py`

#### Covariance Model
- **URL**: `/family/{acc}/cm`
- **Methods**: GET
- **Description**: Download covariance model file
- **Tests**: `test_family.py`

#### Regions
- **URL**: `/family/{acc}/regions`
- **Methods**: GET
- **Description**: Get seed and full region data
- **Tests**: `test_family.py`, `test_alignment_formats.py`

#### RefSeq Regions
- **URL**: `/family/{acc}/refseq`
- **Methods**: GET
- **Description**: Get RefSeq region annotations
- **Tests**: `test_alignment_formats.py`

#### Structures
- **URL**: `/family/{acc}/structures`
- **Methods**: GET
- **Description**: Get PDB structure mappings
- **Tests**: `test_family.py`

#### Sequences
- **URL**: `/family/{acc}/sequences`
- **Methods**: GET
- **Description**: List sequences in family
- **Tests**: `test_family.py`

### Family Tree Endpoints

#### Tree Data
- **URL**: `/family/{acc}/tree/data`
- **Methods**: GET
- **Description**: Download phylogenetic tree (Newick format)
- **Tests**: `test_alignment_formats.py`

#### Tree Image
- **URL**: `/family/{acc}/tree/image`
- **Methods**: GET
- **Description**: Get tree visualization image
- **Tests**: `test_alignment_formats.py`

#### Tree Page
- **URL**: `/family/{acc}/tree`
- **Methods**: GET
- **Description**: Interactive tree viewer
- **Tests**: `test_family.py`

### Family Visualization Endpoints

#### Secondary Structure Image
- **URL**: `/family/{acc}/image`
- **Methods**: GET
- **Description**: Secondary structure diagram
- **Tests**: `test_family.py`

#### Thumbnail
- **URL**: `/family/{acc}/thumbnail`
- **Methods**: GET
- **Description**: Thumbnail image of structure
- **Tests**: `test_family.py`

#### Sunburst
- **URL**: `/family/{acc}/sunburst`
- **Methods**: GET
- **Description**: Taxonomic distribution sunburst chart
- **Tests**: `test_species_tree.py`

#### VARNA
- **URL**: `/family/{acc}/varna`
- **Methods**: GET
- **Description**: VARNA applet data for structure visualization
- **Tests**: Not currently tested

---

## Clan Endpoints

### Main Clan Page
- **URL**: `/clan/{acc_or_id}`
- **Methods**: GET
- **Formats**: HTML, XML (via `?output=xml`)
- **Examples**:
  - `/clan/CL00001` - By accession
  - `/clan/tRNA` - By ID
- **Tests**: `test_clan.py`

### Clan Data Endpoints

#### Structures
- **URL**: `/clan/{acc}/structures`
- **Methods**: GET
- **Description**: Structure mappings for clan families
- **Tests**: `test_clan.py`

---

## Genome Endpoints

### Main Genome Page
- **URL**: `/genome/{ncbi_id}`
- **Methods**: GET
- **Examples**:
  - `/genome/511145` - E. coli K-12
  - `/genome/559292` - S. cerevisiae
- **Tests**: `test_genome.py`

### Genome Data Endpoints

#### GFF Download
- **URL**: `/genome/{ncbi_id}/gff/{auto_genome}`
- **Methods**: GET
- **Description**: Download genome annotations in GFF3 format
- **Tests**: `test_genome.py`

---

## Motif Endpoints

### Main Motif Page
- **URL**: `/motif/{acc_or_id}`
- **Methods**: GET
- **Formats**: HTML, XML (via `?output=xml`)
- **Examples**:
  - `/motif/RM00001` - By accession
  - `/motif/KINK-TURN` - By ID
- **Tests**: `test_motif.py`

---

## Browse Endpoints

### Browse Index
- **URL**: `/browse`
- **Methods**: GET
- **Description**: Main browse page with links to all browse options
- **Tests**: `test_browse.py`

### Browse Families

#### All Families
- **URL**: `/families`
- **Methods**: GET
- **Tests**: `test_browse.py`

#### By Letter
- **URL**: `/families/{letter}`
- **Methods**: GET
- **Examples**: `/families/A`, `/families/T`
- **Tests**: `test_browse.py`

#### By Range
- **URL**: `/families/{from}/{to}`
- **Methods**: GET
- **Description**: Browse families in numeric range
- **Tests**: Not currently tested

#### With Structures
- **URL**: `/families/with_structure`
- **Methods**: GET
- **Description**: Families with 3D structure data
- **Tests**: `test_browse.py`

#### Top 20
- **URL**: `/families/top20`
- **Methods**: GET
- **Description**: 20 largest families by number of sequences
- **Tests**: `test_browse.py`

### Browse Clans
- **URL**: `/clans`
- **Methods**: GET
- **Tests**: `test_browse.py`

### Browse Genomes

#### All Genomes
- **URL**: `/genomes`
- **Methods**: GET
- **Tests**: `test_browse.py`, `test_genome.py`

#### By Kingdom
- **URL**: `/genomes/{kingdom}`
- **Methods**: GET
- **Kingdoms**: Bacteria, Eukaryota, Archaea, Viruses
- **Examples**: `/genomes/Bacteria`
- **Tests**: `test_browse.py`, `test_genome.py`

### Browse Motifs
- **URL**: `/motifs`
- **Methods**: GET
- **Tests**: `test_browse.py`, `test_motif.py`

### Browse Articles
- **URL**: `/articles`
- **Methods**: GET
- **Description**: Browse Wikipedia-annotated families
- **Tests**: `test_browse.py`

---

## Search Endpoints

### Search Index
- **URL**: `/search`
- **Methods**: GET
- **Description**: Main search page with all search forms
- **Tests**: `test_search.py`

### Sequence Search

#### Submit Search
- **URL**: `/search/sequence`
- **Methods**: POST
- **Parameters**:
  - `sequence`: RNA/DNA sequence (max ~7,000 nt)
- **Returns**: Job ID or redirects to results
- **Tests**: `test_search.py`

#### Get Results
- **URL**: `/search/sequence/{job_id}`
- **Methods**: GET
- **Formats**: HTML, JSON, XML, GFF3, TSV
- **Tests**: `test_search.py`

### Batch Search
- **URL**: `/search/batch`
- **Methods**: GET, POST
- **Description**: Upload FASTA file with multiple sequences
- **Parameters**:
  - `file`: FASTA file (max 1,100 sequences)
  - `email`: Email for results notification
- **Tests**: `test_search.py`

### Keyword Search
- **URL**: `/search/keyword`
- **Methods**: GET
- **Parameters**:
  - `query`: Search term
- **Description**: Text search across Rfam entries, Wikipedia, literature
- **Tests**: `test_search.py`

### Taxonomy Search
- **URL**: `/search/taxonomy`
- **Methods**: GET
- **Parameters**:
  - `query`: Species name or taxonomy query (supports AND, OR, NOT)
- **Tests**: `test_search.py`

### Type Search
- **URL**: `/search/type`
- **Methods**: GET
- **Parameters**:
  - `query`: RNA type (e.g., "rRNA", "snRNA", "snoRNA")
- **Tests**: `test_search.py`

### Jump/Smart Search
- **URL**: `/jump`
- **Methods**: GET
- **Parameters**:
  - `entry`: Any identifier (accession, ID, sequence accession)
- **Description**: Guesses entry type and redirects appropriately
- **Tests**: `test_search.py`

---

## Sequence Endpoints

### Sequence Hits Page
- **URL**: `/sequence/{accession}`
- **Methods**: GET
- **Description**: Show Rfam hits for a sequence
- **Examples**: `/sequence/AJ634207`
- **Tests**: `test_sequence.py`

### Sequence Hits Fragment
- **URL**: `/sequence/{accession}/hits`
- **Methods**: GET
- **Description**: Just the hits table (fragment)
- **Tests**: `test_sequence.py`

### Sequence Lookup
- **URL**: `/sequence?entry={accession}`
- **Methods**: GET
- **Tests**: `test_sequence.py`

---

## Structure Endpoints

### PDB File Download
- **URL**: `/structure/{pdb_id}`
- **Methods**: GET
- **Description**: Download PDB structure file
- **Examples**: `/structure/1GID`, `/structure/1QVG`
- **Tests**: `test_sequence.py`
- **⚠️ STATUS**: **BROKEN** - Returns 500 errors and times out (as of Dec 2025)
- **Note**: This endpoint exists in the codebase but is not functional on the live site. Test is skipped. Django rewrite should fix or remove this endpoint.

### AstexViewer
- **URL**: `/structure/{pdb_id}/av`
- **Methods**: GET
- **Description**: AstexViewer applet for structure visualization
- **Examples**: `/structure/1QVG/av`
- **Tests**: `test_sequence.py`
- **✅ STATUS**: Working correctly

---

## Tree and Visualization Endpoints

### Species Tree
- **URL**: `/speciestree`
- **Methods**: GET
- **Description**: Interactive species tree viewer
- **Tests**: `test_species_tree.py`

### MSA Viewer
- Typically embedded in family pages
- **Tests**: `test_species_tree.py`

---

## Static Pages

### Home Page
- **URL**: `/`
- **Methods**: GET
- **Tests**: `test_static_pages.py`

### Help Pages
- **URL**: `/help`
- **Methods**: GET
- **Tests**: `test_static_pages.py`

### Special Content Pages

#### COVID-19
- **URL**: `/covid-19`
- **Methods**: GET
- **Description**: Coronavirus RNA families
- **Note**: The URL is `/covid-19` not `/covid`
- **Tests**: `test_static_pages.py`

#### Viruses
- **URL**: `/viruses`
- **Methods**: GET
- **Description**: Viral RNA families
- **Tests**: `test_static_pages.py`

#### MicroRNA
- **URL**: `/microrna`
- **Methods**: GET
- **Description**: microRNA resources
- **Tests**: `test_static_pages.py`

#### Rfam 20
- **URL**: `/rfam20`
- **Methods**: GET
- **Description**: 20th anniversary content
- **Tests**: `test_static_pages.py`

#### 3D Families
- **URL**: `/3d`
- **Methods**: GET
- **Description**: Families with 3D structure data
- **Tests**: `test_static_pages.py`

### Utility Endpoints

#### Status
- **URL**: `/status`
- **Methods**: GET
- **Description**: Health check endpoint
- **Tests**: `test_static_pages.py`

#### Robots.txt
- **URL**: `/robots.txt`
- **Methods**: GET
- **Tests**: `test_static_pages.py`

---

## API Formats

### JSON API
- **Method**: Send `Accept: application/json` header
- **Available for**:
  - Family pages
- **Structure**:
  ```json
  {
    "rfam": {
      "acc": "RF00001",
      "id": "5S_rRNA",
      "description": "...",
      "curation": { ... },
      "cm": { ... },
      "release": { ... }
    }
  }
  ```
- **Tests**: `test_family.py`

### XML API
- **Method**: Send `Accept: text/xml` header OR use `?output=xml` parameter
- **Available for**:
  - Family pages
  - Clan pages
  - Motif pages
- **Structure**:
  ```xml
  <rfam release="15.00" release_date="2024-09-10">
    <entry entry_type="Rfam" accession="RF00001" id="5S_rRNA">
      <description>...</description>
      <curation_details>...</curation_details>
      <cm_details>...</cm_details>
    </entry>
  </rfam>
  ```
- **Tests**: `test_family.py`, `test_clan.py`, `test_motif.py`

### GFF3 Format
- **Available for**:
  - Genome annotations
  - Search results
- **Tests**: `test_genome.py`, `test_search.py`

---

## Notes

### URL Parameters

Common parameters across endpoints:
- `output=xml` - Request XML format
- `format={format}` - Specify alignment/export format
- `seq_start={n}` - Sequence start coordinate
- `seq_end={n}` - Sequence end coordinate

### Content Negotiation

The site supports content negotiation via:
1. **Accept header** (preferred):
   - `Accept: application/json`
   - `Accept: text/xml`
   - `Accept: text/html`
2. **Query parameter**:
   - `?output=xml`

### Redirects

Some endpoints may redirect:
- Alignment downloads may redirect to FTP
- ID lookups may redirect to accession-based URLs
- Jump search redirects to appropriate entity page

### Rate Limiting

The live site may implement rate limiting. Consider:
- Adding delays between requests
- Using authentication headers if available
- Running tests sequentially for extensive test runs

---

## Endpoint Coverage Summary

| Category | Tested | Total Known | Coverage |
|----------|--------|-------------|----------|
| Family | 15 | 15 | 100% |
| Clan | 3 | 3 | 100% |
| Genome | 4 | 4 | 100% |
| Motif | 3 | 3 | 100% |
| Browse | 12 | 13 | 92% |
| Search | 7 | 7 | 100% |
| Sequence | 4 | 4 | 100% |
| Static | 8 | 8 | 100% |

**Total Endpoints Tested**: 56+ distinct endpoints

---

## For Django Rewrite

When implementing the Django rewrite, use this document as a checklist:

1. ✅ Implement endpoint
2. ✅ Ensure URL routing matches
3. ✅ Support all content types (HTML, JSON, XML)
4. ✅ Handle query parameters
5. ✅ Implement proper error codes (404, 400, etc.)
6. ✅ Run corresponding tests
7. ✅ Verify behavior matches Perl/Catalyst site

Priority endpoints (most critical):
1. `/family/{acc}` (JSON, XML, HTML)
2. `/search/*`
3. `/browse/*`
4. `/family/{acc}/alignment`
5. `/genome/{id}`
