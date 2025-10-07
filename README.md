# RHOAI Container Image Reporter

A practical Python script for generating ad-hoc reports on RHOAI (Red Hat OpenShift AI) container images across different version combinations.

## Overview

This tool extracts and analyzes container image data from two key sources:
- **RHOAI Build Config**: Infrastructure images from OLM catalogs (operators, controllers, services)
- **Disconnected Install Helper**: Workload images for air-gapped deployments (notebooks, training environments)

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Basic usage (uses latest version)
./rhoai_reporter.py

# Specific version
./rhoai_reporter.py --rhoai-version 2.25 --ocp-version 4.20

# Generate JSON output
./rhoai_reporter.py --format json --output report.json

# Compare versions
./rhoai_reporter.py --rhoai-version 2.25 --compare-with 2.24
```

### Authentication

For higher rate limits, set a GitHub token:
```bash
export GITHUB_TOKEN=your_token_here
```

## Features

### Executive Summary
- Total image counts (infrastructure vs workload)
- Registry distribution and trust levels
- Base OS breakdown (RHEL8, RHEL9, UBI)
- Component overview with functional categorization

### Detailed Analysis
- **Infrastructure Components**: Platform core, model serving, data pipelines, distributed computing
- **Workload Components**: Development environments, ML runtimes, specialized AI frameworks
- **Registry Analysis**: Trusted vs community registries
- **Security Insights**: Deprecated images, unverified sources, recommendations

### Output Formats
- **Markdown**: Human-readable reports with tables and sections
- **JSON**: Structured data for programmatic access

## Example Output

```markdown
# RHOAI 2.25 / OCP 4.20 Container Image Report

## Summary
- **Total Images**: 247 (142 infrastructure + 105 workload)
- **Registries**: registry.redhat.io (142), quay.io (105)
- **Base OS**: RHEL8 (180), RHEL9 (67)
- **Estimated Size**: ~24.7GB total download
- **Components**: 8 functional areas identified

## Component Overview
| Component              | Images | Type                    | Description                              |
|------------------------|--------|-------------------------|------------------------------------------|
| Development Environment| 67     | Workload                | Interactive development and experiment...|
| Model Serving         | 45     | Infrastructure          | ML model deployment and inference        |
| Platform Core         | 23     | Infrastructure          | Core platform services and user inter...|
```

## Architecture

```
GitHub API ──┐
             ├─→ Multi-Source Parser ──→ Image Analyzer ──→ Report Generator ──→ Output
             │   (OLM + Markdown)       (Classification)    (Markdown/JSON)
Rate Limiting│
```

### Core Components

1. **GitHubAPIClient**: Fetches data from both repositories with rate limiting
2. **OLMCatalogParser**: Extracts images from YAML catalog files
3. **DisconnectedHelperParser**: Parses markdown image lists
4. **ImageAnalyzer**: Classifies images and performs security analysis
5. **ReportGenerator**: Creates formatted reports

## Configuration

Edit `config.yaml` to customize:

```yaml
repositories:
  build_config: "red-hat-data-services/RHOAI-Build-Config"
  disconnected_helper: "red-hat-data-services/rhoai-disconnected-install-helper"

defaults:
  output_format: "markdown"
  include_security_analysis: true
  cache_duration: 3600

github:
  token: null  # Set via GITHUB_TOKEN environment variable
```

## Development

### Project Structure
```
├── rhoai_reporter.py          # Main CLI application
├── src/
│   ├── github_client.py       # GitHub API client
│   ├── parsers.py             # OLM and markdown parsers
│   ├── analyzer.py            # Image analysis and classification
│   ├── reporter.py            # Report generation
│   ├── models.py              # Data models
│   └── exceptions.py          # Custom exceptions
├── requirements.txt           # Python dependencies
├── config.yaml               # Configuration
└── README.md                 # This file
```

### Testing

```bash
# Test with known version
./rhoai_reporter.py --rhoai-version 2.24 --ocp-version 4.19

# Generate test report
./rhoai_reporter.py --format json --output test_report.json

# Compare versions for validation
./rhoai_reporter.py --rhoai-version 2.25 --compare-with 2.24
```

## Error Handling

The tool handles common failure modes gracefully:
- **Missing versions**: Clear error messages for unsupported combinations
- **Network issues**: Retry logic and rate limiting for GitHub API
- **Malformed data**: Continues processing despite parsing errors
- **Authentication**: Works without token (with rate limits) or with token

## Evolution Path

This basic implementation validates the data extraction approach and provides immediate value. Future enhancements based on usage:

- **Week 2-3**: Web interface, automated CVE checking
- **Month 2**: Database storage, REST API, CI/CD integration
- **Month 3+**: Enterprise features from comprehensive plan (see `tasks.md`)

## Related Documentation

- `context.md`: Detailed analysis of data sources and repository structure
- `tasks.md`: Comprehensive enterprise implementation plan
- `basic.md`: Senior engineering assessment and this implementation plan

## Success Metrics

- ✅ Generate useful reports in <30 seconds
- ✅ Handle missing versions gracefully
- ✅ Classify >90% of images correctly
- ✅ Provide actionable security insights
- ✅ Validate feasibility of comprehensive approach