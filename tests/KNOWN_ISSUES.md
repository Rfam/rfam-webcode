# Known Issues with Live Rfam Site

This document tracks issues discovered during testing of the live Rfam website (https://rfam.org). These represent opportunities for improvement in the Django rewrite.

## Broken Endpoints

### `/structure/{pdb_id}` - PDB File Download

**Status**: ⚠️ BROKEN

**Issue**: This endpoint returns 500 Internal Server Error and times out when attempting to download PDB structure files.

**Tested URLs**:
- `/structure/1GID` → 500 error + timeout
- `/structure/1QVG` → 500 error + timeout
- `/structure/4V9I` → 500 error + timeout

**Root Cause**: Likely an issue with the external PDB file retrieval configuration (`pdbFileUrl` in the Catalyst controller) or the external PDB server being unreachable.

**Code Reference**: `RfamWeb/lib/RfamWeb/Controller/Structure.pm` lines 67-109

**Related Working Endpoint**: `/structure/{pdb_id}/av` (AstexViewer) works correctly

**Test Status**: Test is skipped with `@pytest.mark.skip` to avoid timeouts

**Recommendation for Django Rewrite**:
1. **Option A**: Fix the endpoint by:
   - Using a reliable PDB file source (e.g., RCSB PDB API)
   - Adding proper error handling
   - Implementing timeout protection
2. **Option B**: Remove the endpoint and direct users to external PDB resources (PDBe, RCSB, etc.)
3. **Option C**: Implement a redirect to PDBe download URLs instead of proxying

**Impact**: Low - Users can access PDB structures via external links already present on family structure pages

---

### `/family/{acc}/refseq` - RefSeq Regions

**Status**: ⚠️ BROKEN

**Issue**: This endpoint returns 500 Internal Server Error.

**Tested URLs**:
- `/family/RF00001/refseq` → 500 error

**Test Status**: Test accepts 500 status code to document current state

**Recommendation for Django Rewrite**: Fix or remove this endpoint

---

### `/family/{acc}/regions` - Family Regions

**Status**: ⚠️ ACCESS RESTRICTED

**Issue**: This endpoint returns 403 Forbidden.

**Tested URLs**:
- `/family/RF00001/regions` → 403 Forbidden

**Root Cause**: Endpoint may require authentication or is intentionally restricted

**Test Status**: Test accepts 403 status code

**Recommendation for Django Rewrite**:
- If this should be public, remove restrictions
- If this should be private, implement proper authentication
- Consider if this endpoint is still needed

---

## Endpoints That May Not Exist

Some endpoints are mentioned in the codebase but may not be deployed or accessible:

### Jump Search - 404 on Some Queries

**Status**: ⚠️ Partially Working

**Issue**: The `/jump` endpoint returns 404 for some query formats tested.

**Test Status**: Tests accept both success and 404 responses

**Recommendation**: Verify all intended redirect patterns work in Django rewrite

---

## Performance Issues

### Slow Alignment Downloads

**Status**: ℹ️ Informational

**Issue**: Large family alignments can take significant time to download and format

**Test Status**: These tests are marked with `@pytest.mark.slow`

**Recommendation**: Consider:
- Caching formatted alignments
- Async/background processing for large families
- Progress indicators for downloads
- Size limits with warnings

---

## Test Suite Statistics

- **Total Tests**: 108
- **Passing**: 107
- **Skipped**: 1 (broken PDB download endpoint)
- **Failed**: 0

---

## How to Use This Document

### For Testing

When running tests, you can:
```bash
# See which tests are skipped and why
pytest -v -rs

# Run only skipped tests (to check if they're fixed)
pytest --only-skipped
```

### For Django Development

1. **High Priority**: Focus on implementing working endpoints first
2. **Medium Priority**: Fix broken endpoints (like `/structure/{pdb_id}`)
3. **Low Priority**: Deprecated or rarely-used features

### Updating This Document

When you discover new issues or fix existing ones:

1. Add new issues with same format:
   - Status indicator (⚠️ ❌ ℹ️ ✅)
   - Clear description
   - Test URLs
   - Root cause (if known)
   - Recommendation

2. Mark fixed issues:
   - Update status to ✅ FIXED
   - Add "Fixed in: Django version X.Y"
   - Keep for historical reference

---

## Contributing

If you discover additional issues:

1. Document the issue here
2. Update relevant test files
3. Add skip/xfail markers if needed
4. Update ENDPOINTS.md with status indicators

---

Last Updated: December 9, 2025
