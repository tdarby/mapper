# RHOAI Container Image Reporter - Basic Implementation Plan

## Senior Engineering Assessment

### Critical Analysis of the Comprehensive Approach

**The comprehensive 6-phase approach documented in `tasks.md` is over-engineered for initial needs:**

❌ **Problems with the comprehensive approach:**
- **12-week timeline** with no working solution until Phase 3-4
- **High complexity** requiring APIs, databases, ML models, dashboards
- **Resource intensive** needing dedicated team and infrastructure
- **Risk of project stall** due to scope creep and complexity
- **No early validation** of data sources and parsing feasibility

✅ **Senior Engineering Principles:**
- **Start simple, deliver value early** - Build MVP that solves 80% of problems in 20% of time
- **Prove the concept first** - Validate data extraction before building enterprise infrastructure
- **Iterate based on real usage** - See what users actually need vs. assumptions
- **Fail fast and cheap** - Test approach with minimal investment

---

## Basic Script Implementation Plan

### Overview
Build a single Python script that generates ad-hoc reports for RHOAI/OCP version combinations. This validates the data extraction approach and provides immediate value while informing future development.

### Core Requirements

```bash
# Basic usage
python rhoai_reporter.py --rhoai-version 2.25 --ocp-version 4.20

# Use latest version (default)
python rhoai_reporter.py

# Generate JSON output
python rhoai_reporter.py --format json --output report.json

# Compare versions
python rhoai_reporter.py --rhoai-version 2.25 --compare-with 2.24
```

### Technical Architecture

#### Data Sources
1. **RHOAI Build Config** (via GitHub API)
   - `/catalog/rhoai-X.XX/vX.XX/rhods-operator/catalog.yaml`
   - `/pcc/catalog-vX.XX.yaml` (fallback)

2. **Disconnected Install Helper** (via GitHub API)
   - `/rhoai-X.XX.md`

#### Core Components

```python
class RHOAIReporter:
    def __init__(self):
        self.github_client = GitHubAPIClient()
        self.olm_parser = OLMCatalogParser()
        self.markdown_parser = DisconnectedHelperParser()

    def generate_report(self, rhoai_version: str, ocp_version: str = None) -> Report:
        # Fetch data from both sources
        # Parse and extract image data
        # Analyze and categorize
        # Generate structured report
```

### Implementation Details

#### Phase 1: Data Fetching (Day 1)
**Goal**: Reliable access to both data sources

```python
class GitHubAPIClient:
    def get_olm_catalog(self, rhoai_version: str, ocp_version: str) -> str:
        """Fetch OLM catalog YAML content"""

    def get_disconnected_helper(self, rhoai_version: str) -> str:
        """Fetch disconnected helper markdown content"""

    def get_latest_versions(self) -> tuple[str, str]:
        """Determine latest RHOAI and OCP versions available"""
```

**Technical Tasks:**
- [ ] GitHub API authentication handling
- [ ] File path resolution for different version formats
- [ ] Caching for repeated runs
- [ ] Error handling for missing files/versions

#### Phase 2: Data Parsing (Day 1-2)
**Goal**: Extract image data from both sources

```python
class OLMCatalogParser:
    def parse_catalog(self, yaml_content: str) -> List[ImageReference]:
        """Extract images from OLM catalog YAML"""

    def extract_bundle_images(self, bundle_data: dict) -> List[str]:
        """Get bundle and related images"""

class DisconnectedHelperParser:
    def parse_markdown(self, md_content: str) -> List[ImageReference]:
        """Extract images from markdown lists"""

    def categorize_images(self, images: List[str]) -> Dict[str, List[str]]:
        """Group images by category (notebooks, training, etc.)"""
```

**Technical Tasks:**
- [ ] YAML parsing with `pyyaml.safe_load_all()`
- [ ] Regex patterns for markdown image extraction
- [ ] Image URL validation and normalization
- [ ] Source attribution for each image

#### Phase 3: Analysis and Classification (Day 2)
**Goal**: Meaningful categorization and insights

```python
class ImageAnalyzer:
    def classify_images(self, images: List[ImageReference]) -> Classification:
        """Categorize as infrastructure vs workload"""

    def analyze_registries(self, images: List[ImageReference]) -> RegistryAnalysis:
        """Break down by registry and namespace"""

    def detect_security_patterns(self, images: List[ImageReference]) -> SecurityInsights:
        """Identify potential security concerns"""
```

**Classification Rules:**
- **Infrastructure**: `registry.redhat.io/rhods/*`, `*-operator*`, `*-controller*`
- **Workload**: `quay.io/modh/*`, `*-notebook*`, `*-training*`
- **Base OS Detection**: `-rhel8`, `-rhel9`, `-ubi`

#### Phase 4: Report Generation (Day 2)
**Goal**: Human-readable and actionable output

```python
class ReportGenerator:
    def generate_summary_report(self, analysis: Analysis) -> str:
        """Create executive summary with key metrics"""

    def generate_detailed_report(self, analysis: Analysis) -> str:
        """Full breakdown by component and category"""

    def generate_security_report(self, analysis: Analysis) -> str:
        """Security-focused analysis"""
```

### Report Structure

#### Executive Summary
```markdown
# RHOAI 2.25 / OCP 4.20 Container Image Report

## Summary
- **Total Images**: 247 (142 infrastructure + 105 workload)
- **Registries**: registry.redhat.io (142), quay.io (105)
- **Base OS**: RHEL8 (180), RHEL9 (67)
- **Image Size**: ~15.2GB total download

## Key Changes from 2.24
- Added 12 new notebook images
- Updated 8 model serving components
- Deprecated 3 legacy training images
```

#### Detailed Breakdown
```markdown
## Infrastructure Components (142 images)
### Platform Core (23 images)
- odh-operator: registry.redhat.io/rhods/odh-operator@sha256:abc123...
- odh-dashboard: registry.redhat.io/rhods/odh-dashboard@sha256:def456...

### Model Serving (45 images)
- ModelMesh ecosystem: 12 images
- KServe controllers: 8 images
- Serving runtimes: 25 images

## Workload Components (105 images)
### Development Environments (67 images)
- Jupyter notebooks: 45 images
- VS Code workbenches: 12 images
- Specialized IDEs: 10 images

### Training Runtimes (38 images)
- TensorFlow: 15 images
- PyTorch: 12 images
- CUDA environments: 11 images
```

#### Security Analysis
```markdown
## Security Analysis
### Registry Distribution
- **Trusted Red Hat**: 142 images (57%)
- **Community/ModH**: 105 images (43%)

### Potential Concerns
- 12 images using deprecated base layers
- 3 images from unverified sources
- 5 images missing recent security updates

### Recommendations
- Migrate deprecated base layers before next release
- Verify community image sources
- Update images with known CVEs
```

### Implementation Timeline

**Day 1 (4-6 hours)**:
- Basic GitHub API client
- OLM catalog YAML parsing
- Disconnected helper markdown parsing
- Simple console output

**Day 2 (4-6 hours)**:
- Image classification logic
- Report generation (markdown format)
- Error handling and validation
- Command-line interface

**Total Effort**: 1-2 days vs. 12 weeks for comprehensive approach

### Technical Specifications

#### Dependencies
```python
# requirements.txt
requests>=2.28.0
pyyaml>=6.0
click>=8.0        # CLI interface
rich>=12.0        # Pretty console output
tabulate>=0.9.0   # Table formatting
```

#### Configuration
```yaml
# config.yaml (optional)
repositories:
  build_config: "red-hat-data-services/RHOAI-Build-Config"
  disconnected_helper: "red-hat-data-services/rhoai-disconnected-install-helper"

defaults:
  output_format: "markdown"
  include_security_analysis: true
  cache_duration: 3600  # 1 hour

github:
  token: "${GITHUB_TOKEN}"  # Optional for rate limiting
```

#### Error Handling Strategy
```python
class RHOAIReporterError(Exception):
    """Base exception for reporter errors"""

class VersionNotFoundError(RHOAIReporterError):
    """Requested RHOAI/OCP version combination not available"""

class DataParsingError(RHOAIReporterError):
    """Failed to parse catalog or markdown data"""
```

### Validation and Testing

#### Unit Tests
- Mock GitHub API responses
- Test parsing with known-good data
- Validate classification rules
- Test report generation

#### Integration Tests
- Real API calls with current versions
- End-to-end report generation
- Performance testing with large catalogs

#### Acceptance Criteria
- [ ] Generate report for RHOAI 2.25/OCP 4.20 in <30 seconds
- [ ] Handle missing version gracefully
- [ ] Classify >90% of images correctly
- [ ] Produce actionable security insights

### Future Evolution Path

#### Version 2 (Week 2-3)
- Web interface for non-technical users
- Historical trend analysis
- Automated CVE checking
- Slack/email report delivery

#### Version 3 (Month 2)
- Database storage for historical data
- REST API for programmatic access
- Integration with CI/CD pipelines
- Custom report templates

#### Enterprise Version (Month 3+)
- Real-time monitoring and alerting
- Multi-product support (beyond RHOAI)
- Advanced analytics and ML insights
- Full implementation of comprehensive approach

### Success Metrics

#### Immediate (Week 1)
- Working script that generates useful reports
- Positive feedback from initial users
- Validation of data extraction approach

#### Short-term (Month 1)
- Regular usage by multiple teams
- Discovery of additional use cases
- Clear requirements for enhanced features

#### Long-term (Quarter 1)
- Foundation for enterprise solution
- Proven ROI and user adoption
- Technical feasibility validation

---

## Decision: Start with Basic Implementation

**Recommendation**: Build the basic script first to:
1. **Validate the data sources** and parsing approach
2. **Deliver immediate value** to users waiting for this capability
3. **Learn from real usage** before investing in enterprise infrastructure
4. **Reduce project risk** by proving concepts incrementally

The comprehensive approach documented in `tasks.md` remains valuable as a **north star architecture**, but should be implemented only after validating demand and feasibility with the basic script.

**Next Steps**: Implement the basic script as described above, gather user feedback, then selectively implement components from the comprehensive plan based on actual requirements.