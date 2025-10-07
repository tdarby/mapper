# RHOAI Container Image Functional Mapping System - Development Tasks

## Project Overview

This project aims to create a repeatable, automated process for mapping functional roles within the RHOAI platform to their corresponding container images. The system will provide comprehensive understanding of the complete composition of each functional area, enabling better dependency tracking, security analysis, and lifecycle management.

## System Architecture

### Data Flow
```
RHOAI Build Config Repository ──┐
                                ├─→ Multi-Source Parser → Component Mapper → Functional Analyzer → Output APIs/Reports
Disconnected Install Helper ────┘
```

### Core Components
1. **Multi-Source Catalog Parser**: Extract image metadata from OLM catalogs and disconnected helper repositories
2. **Component Mapper**: Map images to upstream components and repositories with infrastructure/workload classification
3. **Functional Analyzer**: Group components by platform functions across both infrastructure and workload images
4. **API Service**: Provide queryable interfaces for the mapping data with multi-source support
5. **Automation Pipeline**: Keep mappings updated as both repositories change

---

## Phase 1: Data Extraction and Parsing Infrastructure

### Task 1.1: Multi-Source Catalog Parser Development
**Priority**: High
**Estimated Effort**: 7-10 days
**Dependencies**: None

**Acceptance Criteria**:
- Parse all YAML catalog files in `/catalog/` and `/pcc/` directories (RHOAI Build Config)
- Parse markdown image lists in disconnected helper repository
- Extract container image references with full metadata from both sources
- Handle multiple RHOAI versions (2.6-2.24) and OCP versions (4.14-4.20)
- Support both bundle images and related images (OLM) and workload images (disconnected helper)
- Classify images as infrastructure vs. workload based on source
- Merge and deduplicate images across sources
- Output structured data (JSON/YAML) with source attribution

**Technical Tasks**:
- [ ] Create YAML parser for OLM catalog format
- [ ] Create markdown parser for disconnected helper image lists
- [ ] Implement image reference extraction logic for both sources
- [ ] Build version-aware parsing (handle schema variations)
- [ ] Add validation for required fields (image, SHA256, name)
- [ ] Implement data merging and deduplication logic
- [ ] Add source attribution and classification (infrastructure vs. workload)
- [ ] Create unit tests for parser edge cases (both sources)
- [ ] Add error handling for malformed catalogs and markdown files

**Automation Requirements**:
- CLI interface for batch processing (multiple repositories)
- Configuration file for custom parsing rules and repository locations
- Logging and metrics collection (per source and combined)
- Docker containerization for CI/CD
- Support for local and remote repository access

### Task 1.2: Image Metadata Enrichment
**Priority**: High
**Estimated Effort**: 4-6 days
**Dependencies**: Task 1.1

**Acceptance Criteria**:
- Extract semantic names from `relatedImages` sections (OLM) and markdown headers (disconnected helper)
- Parse image naming conventions (registry, namespace, component, variant) for both sources
- Identify image families and relationships across infrastructure and workload images
- Cross-reference with Tekton pipeline metadata and ImageSetConfiguration examples
- Enrich with source-specific metadata (bundle relationships vs. notebook categories)

**Technical Tasks**:
- [ ] Implement image URL parsing (registry/namespace/name@digest) for both sources
- [ ] Build semantic name mapping logic (OLM relatedImages vs. markdown categories)
- [ ] Create image family grouping algorithm across infrastructure and workload images
- [ ] Add Tekton pipeline metadata integration and ImageSetConfiguration parsing
- [ ] Develop image relationship detection (bundle chains vs. notebook variants)
- [ ] Create metadata validation rules for multi-source data
- [ ] Implement cross-source image relationship detection

---

## Phase 2: Component Classification and Mapping

### Task 2.1: Multi-Source Component Classification Engine
**Priority**: High
**Estimated Effort**: 8-12 days
**Dependencies**: Task 1.2

**Acceptance Criteria**:
- Automatic component detection based on naming patterns for both infrastructure and workload images
- Mapping to upstream repositories and documentation with source-aware logic
- Functional category assignment (Platform, Serving, Pipelines, Development Environments, etc.)
- Infrastructure vs. workload classification with confidence scoring
- Cross-source component relationship detection

**Technical Tasks**:
- [ ] Build pattern matching engine for component identification (infrastructure + workload)
- [ ] Create dual-taxonomy classification rules (infrastructure vs. workload components)
- [ ] Implement upstream repository mapping logic with source awareness
- [ ] Add functional category assignment algorithm covering development environments
- [ ] Develop confidence scoring system for cross-source classifications
- [ ] Create machine learning model for classification improvement across both sources
- [ ] Build manual override mechanism for edge cases and cross-source conflicts
- [ ] Implement infrastructure-workload relationship mapping

**Data Sources**:
- Component naming patterns from OLM catalog analysis and disconnected helper categorization
- GitHub repository metadata for both infrastructure and workload components
- Documentation links and descriptions across multiple component types
- Community knowledge base including notebook and development environment patterns
- ImageSetConfiguration examples and Tekton pipeline metadata

### Task 2.2: Functional Area Mapping
**Priority**: High
**Estimated Effort**: 4-6 days
**Dependencies**: Task 2.1

**Acceptance Criteria**:
- Group components into functional areas (Dashboard, Model Serving, etc.)
- Define component dependencies and relationships
- Create functional area composition reports
- Support multi-version functional area analysis

**Technical Tasks**:
- [ ] Design functional area taxonomy
- [ ] Implement component-to-function mapping logic
- [ ] Build dependency analysis engine
- [ ] Create composition reporting system
- [ ] Add version comparison capabilities
- [ ] Develop functional area health metrics

**Functional Areas to Map**:

**Infrastructure Functions**:
- Platform Core (Operator, Dashboard, Authentication)
- Notebook Management Infrastructure (JupyterHub, Notebook Controllers)
- Model Serving Infrastructure (ModelMesh, KServe controllers)
- Data Pipeline Infrastructure (Kubeflow Pipelines, Argo, Tekton)
- Distributed Computing Infrastructure (Ray operators, CodeFlare, Training operators)
- Monitoring and Observability (Prometheus, Grafana)

**Workload Functions**:
- Development Environments (Jupyter notebooks, VS Code workbenches, IDEs)
- ML/AI Training Runtimes (TensorFlow, PyTorch, CUDA environments)
- Specialized AI Frameworks (OpenVINO runtimes, TrustyAI tools)
- Data Science Tools (R, Julia, data visualization environments)

---

## Phase 3: API and Data Services

### Task 3.1: REST API Development
**Priority**: Medium
**Estimated Effort**: 5-7 days
**Dependencies**: Task 2.2

**Acceptance Criteria**:
- RESTful API for querying image mappings
- GraphQL endpoint for complex relationship queries
- Real-time data updates via webhooks
- API versioning and backward compatibility

**Technical Tasks**:
- [ ] Design API schema and endpoints
- [ ] Implement REST API with OpenAPI specification
- [ ] Add GraphQL query interface
- [ ] Build real-time update mechanism
- [ ] Create API authentication and authorization
- [ ] Add rate limiting and caching
- [ ] Implement API versioning strategy

**API Endpoints**:
```
GET /api/v1/images/{image-digest}          # Get image details (infrastructure or workload)
GET /api/v1/components/{component-name}    # Get component information with classification
GET /api/v1/functions/{function-area}      # Get functional area composition (infrastructure + workload)
GET /api/v1/versions/{rhoai-version}       # Get version-specific mappings (both sources)
GET /api/v1/sources/{source-type}          # Get source-specific data (olm_catalog or disconnected_helper)
GET /api/v1/classifications/infrastructure # Get all infrastructure components
GET /api/v1/classifications/workload       # Get all workload components
POST /api/v1/query                         # Complex queries via GraphQL with multi-source support
```

### Task 3.2: Database and Storage Design
**Priority**: Medium
**Estimated Effort**: 4-6 days
**Dependencies**: Task 2.2

**Acceptance Criteria**:
- Scalable database schema for image metadata
- Efficient querying for complex relationships
- Data versioning and historical tracking
- Backup and disaster recovery

**Technical Tasks**:
- [ ] Design normalized database schema
- [ ] Implement database migrations system
- [ ] Add indexing strategy for performance
- [ ] Create data versioning mechanism
- [ ] Build backup and recovery procedures
- [ ] Add database monitoring and alerting

**Schema Design**:
- Images table (digest, registry, name, version, metadata, classification, source_type)
- Components table (name, upstream_repo, category, description, component_type)
- Functions table (area, description, criticality, function_type)
- Relationships table (image_id, component_id, function_id, type, source_attribution)
- Versions table (rhoai_version, ocp_version, release_date)
- Sources table (source_type, repository_url, last_updated, file_path)
- Classifications table (image_id, infrastructure_confidence, workload_confidence)

---

## Phase 4: Automation and CI/CD Integration

### Task 4.1: Automated Pipeline Development
**Priority**: High
**Estimated Effort**: 6-8 days
**Dependencies**: Task 3.1

**Acceptance Criteria**:
- Automated processing of repository updates from both RHOAI Build Config and disconnected helper
- CI/CD integration with GitHub Actions/Tekton for multi-repository monitoring
- Scheduled batch processing for comprehensive scans across both sources
- Error handling and notification system with source-specific alerting

**Technical Tasks**:
- [ ] Build GitHub webhook handler for repository changes (both repositories)
- [ ] Create Tekton pipeline for automated multi-source processing
- [ ] Implement incremental vs. full scan logic with source awareness
- [ ] Add error handling and retry mechanisms for multi-repository failures
- [ ] Create notification system for failures/changes with source attribution
- [ ] Build monitoring dashboard for pipeline health across both sources
- [ ] Implement cross-repository synchronization and conflict resolution

**Pipeline Stages**:
1. Multi-repository change detection (Build Config + Disconnected Helper)
2. Parallel catalog parsing and validation (OLM + Markdown)
3. Cross-source component classification and mapping
4. Data merging and deduplication
5. Database update and versioning with source attribution
6. API cache invalidation and relationship recalculation
7. Notification and reporting with source-specific insights

### Task 4.2: Quality Assurance and Validation
**Priority**: High
**Estimated Effort**: 4-5 days
**Dependencies**: Task 4.1

**Acceptance Criteria**:
- Automated validation of mapping accuracy
- Regression testing for catalog changes
- Data quality metrics and alerting
- Manual review workflow for edge cases

**Technical Tasks**:
- [ ] Build automated validation test suite
- [ ] Create regression testing framework
- [ ] Implement data quality metrics collection
- [ ] Add manual review workflow system
- [ ] Create data drift detection
- [ ] Build alerting for quality issues

---

## Phase 5: Reporting and Visualization

### Task 5.1: Reporting Engine
**Priority**: Medium
**Estimated Effort**: 5-7 days
**Dependencies**: Task 3.2

**Acceptance Criteria**:
- Automated report generation for functional areas
- Security vulnerability mapping reports
- Component dependency analysis reports
- Historical trend analysis

**Technical Tasks**:
- [ ] Design report templates and formats
- [ ] Implement scheduled report generation
- [ ] Add export capabilities (PDF, CSV, JSON)
- [ ] Create report distribution system
- [ ] Build custom report builder interface
- [ ] Add report archival and versioning

**Report Types**:
- Functional Area Composition Report
- Component Vulnerability Assessment
- Dependency Impact Analysis
- Version Migration Guide
- Security Compliance Report

### Task 5.2: Visualization Dashboard
**Priority**: Low
**Estimated Effort**: 6-8 days
**Dependencies**: Task 5.1

**Acceptance Criteria**:
- Interactive web dashboard for exploring mappings
- Dependency graph visualization
- Historical trend charts
- Real-time status monitoring

**Technical Tasks**:
- [ ] Design dashboard UI/UX
- [ ] Implement interactive data visualization
- [ ] Add dependency graph rendering
- [ ] Create real-time data updates
- [ ] Build responsive design for mobile
- [ ] Add user authentication and role-based access

---

## Phase 6: Documentation and Maintenance

### Task 6.1: Documentation and Training
**Priority**: Medium
**Estimated Effort**: 3-4 days
**Dependencies**: Task 5.2

**Technical Tasks**:
- [ ] Create API documentation with examples
- [ ] Write system administration guide
- [ ] Build user manual for dashboard
- [ ] Create troubleshooting guide
- [ ] Add development setup instructions
- [ ] Create video tutorials for common tasks

### Task 6.2: Monitoring and Maintenance Tools
**Priority**: Medium
**Estimated Effort**: 4-5 days
**Dependencies**: Task 6.1

**Technical Tasks**:
- [ ] Implement system health monitoring
- [ ] Add performance metrics collection
- [ ] Create automated maintenance tasks
- [ ] Build capacity planning tools
- [ ] Add log aggregation and analysis
- [ ] Create incident response procedures

---

## Implementation Timeline

### Sprint 1 (Weeks 1-2): Foundation
- Task 1.1: Catalog Parser Development
- Task 1.2: Image Metadata Enrichment

### Sprint 2 (Weeks 3-4): Classification Engine
- Task 2.1: Component Classification Engine
- Task 2.2: Functional Area Mapping

### Sprint 3 (Weeks 5-6): Data Services
- Task 3.1: REST API Development
- Task 3.2: Database and Storage Design

### Sprint 4 (Weeks 7-8): Automation
- Task 4.1: Automated Pipeline Development
- Task 4.2: Quality Assurance and Validation

### Sprint 5 (Weeks 9-10): Reporting
- Task 5.1: Reporting Engine
- Task 5.2: Visualization Dashboard

### Sprint 6 (Weeks 11-12): Documentation and Deployment
- Task 6.1: Documentation and Training
- Task 6.2: Monitoring and Maintenance Tools

---

## Technology Stack Recommendations

### Backend Services
- **Language**: Python 3.9+ or Go 1.19+
- **Framework**: FastAPI (Python) or Gin (Go)
- **Database**: PostgreSQL with TimescaleDB for time-series data
- **Cache**: Redis for API caching
- **Message Queue**: Apache Kafka for event streaming

### Frontend Dashboard
- **Framework**: React with TypeScript
- **Visualization**: D3.js, Chart.js, or Recharts
- **State Management**: Redux Toolkit
- **UI Components**: Material-UI or Ant Design

### Infrastructure
- **Containerization**: Docker with multi-stage builds
- **Orchestration**: Kubernetes with Helm charts
- **CI/CD**: Tekton Pipelines or GitHub Actions
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)

### Development Tools
- **Testing**: pytest (Python) or testify (Go)
- **Code Quality**: SonarQube, ESLint, Black/gofmt
- **Documentation**: Swagger/OpenAPI, GitBook
- **Version Control**: Git with conventional commits

---

## Success Metrics

### Technical Metrics
- **Accuracy**: >95% correct component classification across both infrastructure and workload images
- **Coverage**: 100% of images in both OLM catalogs and disconnected helper lists processed
- **Performance**: <2s API response time for queries across multi-source data
- **Availability**: 99.9% system uptime with multi-repository resilience
- **Data Freshness**: <1 hour lag from repository updates (either source)
- **Cross-Source Consistency**: >99% agreement on overlapping images between sources

### Business Metrics
- **User Adoption**: Number of API calls and dashboard users
- **Time Savings**: Reduced manual analysis time
- **Security Response**: Faster vulnerability impact assessment
- **Compliance**: Automated compliance reporting accuracy

---

## Risk Mitigation

### Technical Risks
- **Schema Changes**: Implement flexible parsing with fallbacks
- **Scale Issues**: Design for horizontal scaling from day one
- **Data Quality**: Implement multiple validation layers
- **Performance**: Add caching and database optimization

### Operational Risks
- **Maintenance Overhead**: Automate all recurring tasks
- **Knowledge Transfer**: Comprehensive documentation and training
- **Security**: Implement security best practices throughout
- **Compliance**: Regular security audits and penetration testing

---

## Future Enhancements

### Phase 7: Advanced Analytics
- Machine learning for anomaly detection
- Predictive analytics for component upgrades
- Automated security impact analysis
- Integration with vulnerability databases

### Phase 8: Ecosystem Integration
- Integration with Red Hat build systems
- Connection to upstream project trackers
- Automated pull request generation for updates
- Cross-platform compatibility analysis

### Phase 9: Community Features
- Public API for community access
- Contribution workflow for community mappings
- Integration with package managers
- Open source component tracking