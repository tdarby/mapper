# RHOAI Container Image Functional Mapping - Implementation Context

This document provides essential context and findings from the analysis of the RHOAI Build Config repository, necessary for implementing the tasks outlined in `tasks.md`. This information was gathered through comprehensive repository analysis and serves as the foundation for building the automated container image functional mapping system.

## Repository Overview

### Primary Source Repository
- **Repository**: `RHOAI-Build-Config` (Red Hat OpenShift AI Build Configuration)
- **Purpose**: Contains operator lifecycle management (OLM) catalogs and build configurations for RHOAI
- **Structure**: File-based catalogs (FBC) organized by version and platform compatibility
- **Scope**: RHOAI versions 2.6-2.24, OpenShift Container Platform versions 4.14-4.20
- **Content**: Infrastructure and operator images, bundle metadata, channel definitions

### Secondary Source Repository
- **Repository**: `rhoai-disconnected-install-helper` (Red Hat OpenShift AI Disconnected Install Helper)
- **Purpose**: Provides supplemental image lists for air-gapped/disconnected RHOAI installations
- **Structure**: Version-specific markdown files with image lists and automation scripts
- **Scope**: RHOAI versions 2.6+ with focus on runtime and workload images
- **Content**: Notebook environments, training frameworks, development tools, CUDA images

### Key Directories and Files

#### RHOAI-Build-Config Repository Structure
```
RHOAI-Build-Config/
├── catalog/                          # Versioned OLM catalogs
│   └── rhoai-X.XX/                  # RHOAI version directories
│       └── vX.XX/                   # OCP version directories
│           └── rhods-operator/
│               └── catalog.yaml     # Main catalog file
├── pcc/                             # Pre-compiled catalogs
│   ├── catalog-vX.XX.yaml          # Consolidated catalogs by OCP version
│   ├── bundle_object_catalog.yaml  # Bundle metadata
│   └── csv_meta_catalog.yaml       # ClusterServiceVersion metadata
├── .tekton/                         # Tekton pipeline configurations
│   └── *.yaml                      # Build and deployment pipelines
├── .github/workflows/               # GitHub Actions workflows
│   └── *.yaml                      # CI/CD automation
├── builds/                          # Build trigger files
│   └── force-trigger*.txt          # Manual build triggers
└── config/
    └── config.yaml                 # Configuration metadata
```

#### rhoai-disconnected-install-helper Repository Structure
```
rhoai-disconnected-install-helper/
├── rhoai-X.XX.md                    # Version-specific image lists
├── rhods-X.XX.md                    # Legacy RHODS version files
├── rhoai-disconnected-helper.sh     # Automation script for image extraction
├── releases.yaml                    # Version and release metadata
├── .github/workflows/               # Automated image list updates
│   └── *.yaml                      # CI/CD for image discovery
└── examples/
    └── ImageSetConfiguration.yaml   # oc-mirror configuration examples
```

## Data Sources and Schema Analysis

### Primary Data Sources

#### 1. OLM Catalog Files (Infrastructure Images)
**Location**: `/catalog/rhoai-X.XX/vX.XX/rhods-operator/catalog.yaml`
**Format**: YAML with OLM schema
**Size**: Large files (900KB-1.2MB+ each)
**Image Types**: Operators, controllers, infrastructure services
**Structure**:
```yaml
schema: olm.package
name: rhods-operator
defaultChannel: stable
icon:
  base64data: [base64-encoded SVG]
  mediatype: image/svg+xml
---
schema: olm.channel
name: stable
entries:
- name: rhods-operator.X.XX.X-X
  replaces: rhods-operator.X.XX.X-X
  skipRange: '>=X.XX.X <X.XX.X'
---
schema: olm.bundle
name: rhods-operator.X.XX.X-X
image: registry.redhat.io/rhods/odh-operator-bundle@sha256:xxx
properties:
- type: olm.gvk
- type: olm.package
- type: olm.csv.metadata
relatedImages:
- image: registry.redhat.io/rhods/component@sha256:xxx
  name: semantic_name
```

#### 2. Pre-compiled Catalogs (PCC)
**Location**: `/pcc/catalog-vX.XX.yaml`
**Purpose**: Consolidated catalogs combining multiple RHOAI versions
**Advantages**: Easier parsing, complete version coverage
**Structure**: Similar to individual catalogs but aggregated

#### 3. Disconnected Helper Image Lists (Workload Images)
**Location**: `/rhoai-X.XX.md` in disconnected install helper repository
**Format**: Markdown with YAML-like image lists
**Size**: Small to medium files (10-50KB each)
**Image Types**: Notebooks, training environments, development tools
**Structure**:
```markdown
# RHOAI 2.25 Images

## Notebook Images
- quay.io/modh/odh-generic-data-science-notebook@sha256:abc123...
- quay.io/modh/cuda-notebooks@sha256:def456...

## Training Images
- quay.io/modh/pytorch-notebook@sha256:ghi789...
- quay.io/modh/tensorflow-notebook@sha256:jkl012...

## ImageSetConfiguration Example
```yaml
apiVersion: mirror.openshift.io/v1alpha2
kind: ImageSetConfiguration
metadata:
  name: rhoai-disconnected
spec:
  mirror:
    additionalImages:
    - name: quay.io/modh/odh-generic-data-science-notebook@sha256:abc123...
```

#### 4. Tekton Pipelines
**Location**: `/.tekton/*.yaml`
**Purpose**: Build automation and image mirroring
**Contains**: Image mirror mappings, SBOM generation, signature validation

### Container Image Metadata Schema

#### Image Reference Format
```
registry.redhat.io/[namespace]/[component]-[variant]@sha256:[digest]
```

**Registry Patterns**:
- `registry.redhat.io/rhods/` - RHODS/earlier RHOAI versions (infrastructure)
- `registry.redhat.io/rhoai/` - Current RHOAI versions (infrastructure)
- `registry.redhat.io/openshift4/` - OpenShift base components
- `quay.io/modh/` - ModH (Operate-First) workload images
- `quay.io/opendatahub/` - Open Data Hub community images

**Naming Conventions**:
- Components typically prefixed with `odh-` (Open Data Hub)
- Variants include `-rhel8`, `-rhel9`, `-v2-rhel8`
- Bundle images end with `-bundle`

#### Extractable Metadata Per Image

**Core Properties**:
- **Image Digest**: SHA256 hash for immutable reference
- **Registry**: Source registry location
- **Component Name**: Parsed from image name
- **Semantic Name**: Human-readable identifier from `relatedImages.name` (OLM) or markdown headers (disconnected helper)
- **Base OS**: RHEL8, RHEL9, UBI variants
- **Image Classification**: Infrastructure (operators, controllers) vs. Workload (notebooks, training)

**Version Information**:
- **RHOAI Version**: 2.6 through 2.24
- **OCP Compatibility**: 4.14 through 4.20
- **Operator Version**: Semantic versioning (e.g., `1.20.1-8`, `2.24.0`)
- **Build Metadata**: Embedded in tags and labels

**Lifecycle Metadata**:
- **Bundle Relationships**: `replaces` chains for upgrades
- **Channel Assignment**: `stable`, `alpha`, `beta`, `eus-X.XX`
- **Skip Ranges**: Version optimization for upgrades
- **Dependencies**: API groups and resource requirements

## Component Classification Schema

### Identified Component Categories

#### Infrastructure Components (from OLM Catalogs)

##### 1. Platform Core
**Components**: Operator, Dashboard, Authentication, Deployer
**Image Patterns**: `odh-operator`, `odh-dashboard`, `odh-deployer`
**Function**: Foundation services and user interface
**Source**: OLM catalogs

##### 2. Notebook Management Infrastructure
**Components**: Notebook controllers, JupyterHub integration
**Image Patterns**: `odh-notebook-controller`, `odh-kf-notebook-controller`
**Function**: Interactive development environment management
**Source**: OLM catalogs

##### 3. Model Serving Infrastructure
**Components**: ModelMesh ecosystem, KServe, serving runtimes
**Image Patterns**: `odh-modelmesh*`, `odh-model-controller`, `odh-mm-rest-proxy`
**Function**: ML model deployment and inference
**Upstream**: https://github.com/kserve/modelmesh
**Source**: OLM catalogs

##### 4. Data Pipeline Infrastructure
**Components**: Kubeflow Pipelines, Data Science Pipelines, Argo
**Image Patterns**: `odh-ml-pipelines*`, `odh-data-science-pipelines*`
**Function**: Workflow orchestration and data processing
**Upstream**: https://github.com/kubeflow/pipelines
**Source**: OLM catalogs

##### 5. Distributed Computing Infrastructure
**Components**: Ray, CodeFlare, Training Operator, Kueue
**Image Patterns**: `odh-kuberay*`, `odh-codeflare*`, `odh-training-operator`
**Function**: Distributed ML training and batch processing
**Upstream**: https://github.com/ray-project/kuberay
**Source**: OLM catalogs

#### Workload Components (from Disconnected Helper)

##### 6. Development Environments
**Components**: Jupyter notebooks, VS Code servers, IDEs
**Image Patterns**: `*-notebook`, `*-workbench`, `code-server*`
**Function**: Interactive development and experimentation
**Source**: Disconnected helper repository

##### 7. ML/AI Training Runtimes
**Components**: TensorFlow, PyTorch, CUDA environments
**Image Patterns**: `tensorflow-*`, `pytorch-*`, `cuda-*`
**Function**: Model training and development environments
**Source**: Disconnected helper repository

##### 8. Specialized AI Frameworks
**Components**: OpenVINO, TrustyAI, serving runtimes
**Image Patterns**: `openvino*`, `trustyai*`, `*-runtime`
**Function**: Specialized model execution and analysis
**Source**: Both OLM catalogs (infrastructure) and disconnected helper (runtimes)

### Component-to-Repository Mapping

```yaml
Component Mappings:
  odh-operator: https://github.com/opendatahub-io/opendatahub-operator
  odh-dashboard: https://github.com/opendatahub-io/odh-dashboard
  odh-notebook-controller: https://github.com/opendatahub-io/notebook-controller
  odh-modelmesh: https://github.com/kserve/modelmesh
  odh-modelmesh-serving: https://github.com/kserve/modelmesh-serving
  odh-ml-pipelines: https://github.com/kubeflow/pipelines
  odh-kuberay: https://github.com/ray-project/kuberay
  odh-codeflare: https://github.com/project-codeflare/codeflare-operator
  odh-training-operator: https://github.com/kubeflow/training-operator
```

## Technical Implementation Insights

### Parsing Challenges and Solutions

#### Large File Handling
**Challenge**: Catalog files can exceed 1MB
**Solution**: Implement streaming parser with offset/limit support
**Code Pattern**:
```python
# Read file in chunks for large catalogs
def read_catalog_chunked(file_path, chunk_size=50):
    with open(file_path) as f:
        while chunk := read_lines(f, chunk_size):
            yield parse_chunk(chunk)
```

#### Schema Variations
**Challenge**: OLM schema evolution across versions
**Solution**: Version-aware parsing with fallback strategies
**Pattern**: Use schema detection and version-specific parsers

#### Multi-document YAML
**Challenge**: Catalogs contain multiple YAML documents
**Solution**: Use `yaml.safe_load_all()` for document iteration

### Data Quality Considerations

#### Semantic Name Mapping
**Location**: `relatedImages[].name` field
**Format**: `odh_component_image`, `ml_pipelines_api_server_image`
**Usage**: Provides explicit component identification beyond image names

#### Image Family Detection
**Pattern**: Group related images by component prefix
**Example**: `odh-modelmesh`, `odh-modelmesh-runtime-adapter`, `odh-modelmesh-serving-controller`

#### Version Consistency
**Validation**: Ensure image versions align with operator bundle versions
**Cross-reference**: Bundle version → component versions → image digests

### Security and Provenance

#### Signature Validation
**Format**: Cosign signatures at `${BASE_URI}:${DIGEST/:/-}.sig`
**Tekton Integration**: Signature validation in promotion workflows
**Storage**: Separate signature artifacts linked to image digests

#### SBOM Generation
**Tool**: `quay.io/konflux-ci/tekton-catalog/task-show-sbom`
**Trigger**: Part of build pipeline automation
**Output**: Software Bill of Materials for vulnerability tracking

#### Build Provenance
**Git Integration**: Commit SHA tracking in build metadata
**Pipeline Records**: Tekton pipeline execution history
**Registry Metadata**: Build timestamp and source information

## Data Processing Pipeline Design

### Recommended Processing Flow

1. **Discovery Phase**
   - Scan `/catalog/` directory structure
   - Identify all RHOAI and OCP version combinations
   - Build processing manifest

2. **Extraction Phase**
   - Parse YAML catalogs using streaming approach
   - Extract bundle and image metadata
   - Validate required fields and relationships

3. **Classification Phase**
   - Apply pattern matching for component identification
   - Map to upstream repositories using lookup tables
   - Assign functional categories and confidence scores

4. **Enrichment Phase**
   - Cross-reference with Tekton metadata
   - Add security and provenance information
   - Calculate relationships and dependencies

5. **Storage Phase**
   - Normalize data for database storage
   - Version and timestamp all records
   - Build indexes for efficient querying

### Error Handling Patterns

#### Malformed YAML
**Detection**: Schema validation against OLM spec
**Recovery**: Log errors, skip malformed entries, continue processing
**Reporting**: Maintain error metrics and alerts

#### Missing Dependencies
**Detection**: Broken image references or missing semantic names
**Recovery**: Use fallback classification methods
**Escalation**: Flag for manual review

#### Version Conflicts
**Detection**: Inconsistent version information across metadata
**Resolution**: Prefer authoritative sources (bundle metadata over filenames)
**Documentation**: Track resolution decisions for auditing

## Automation Integration Points

### Repository Webhooks
**Triggers**: Changes to `/catalog/` or `/pcc/` directories
**Events**: Push to main branch, PR merges, force triggers
**Processing**: Incremental updates for changed files only

### CI/CD Integration
**GitHub Actions**: Existing workflows for validation and promotion
**Tekton Pipelines**: Build automation and image mirroring
**Integration Point**: Add mapping pipeline as post-processing step

### Quality Gates
**Validation**: Schema compliance, data completeness
**Testing**: Regression tests for classification accuracy
**Metrics**: Coverage, accuracy, performance benchmarks

## Performance Considerations

### Scale Metrics
- **OLM Catalog Files**: ~50 files across all versions (infrastructure images)
- **Disconnected Helper Files**: ~20 version files (workload images)
- **Images per OLM Catalog**: 200-400 container images
- **Images per Disconnected File**: 50-150 container images
- **Total Infrastructure Images**: ~15,000-20,000 unique image references
- **Total Workload Images**: ~2,000-5,000 unique image references
- **Combined Total**: ~17,000-25,000 unique image references
- **Processing Time**: Target <5 minutes for full multi-repository scan

### Optimization Strategies
- **Caching**: Cache parsed results with file modification timestamps
- **Parallel Processing**: Process multiple catalogs concurrently
- **Incremental Updates**: Only reprocess changed files
- **Database Indexing**: Optimize queries for common access patterns

## Future Enhancement Opportunities

### Machine Learning Integration
**Training Data**: Classified component mappings from manual review
**Model**: Text classification for component identification
**Features**: Image names, semantic names, repository patterns
**Goal**: Improve classification accuracy and handle edge cases

### Community Integration
**Upstream Sync**: Monitor upstream repository changes
**Pull Request Automation**: Generate updates for new component versions
**Documentation Integration**: Link to component documentation and guides

### Cross-Platform Analysis
**Multi-Product**: Extend to other Red Hat AI/ML products
**Ecosystem Mapping**: Track dependencies across product boundaries
**Compliance**: Automated compliance and license tracking

---

## Implementation Notes

### Getting Started
1. Clone this repository for test data and schema examples
2. Start with PCC files (`/pcc/catalog-*.yaml`) for simpler parsing
3. Use the component classification schema as initial training data
4. Build incrementally following the 6-phase plan in `tasks.md`

### Testing Strategy
- Use this repository as integration test data
- Validate against known component mappings documented here
- Implement regression tests for schema changes
- Performance test with full repository scan

### Success Validation
- Achieve >95% accuracy against manual classification
- Process full repository in <5 minutes
- Detect all major component categories identified in this analysis
- Maintain data freshness within 1 hour of repository updates