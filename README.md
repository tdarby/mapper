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

# Generate JSON output with granular component breakdown
./rhoai_reporter.py --format json --output report.json

# Compare versions
./rhoai_reporter.py --rhoai-version 2.25 --compare-with 2.24

# Use legacy broad classification (less detailed)
./rhoai_reporter.py --no-granular
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

### Granular Component Analysis
- **LLM & Text Generation**: vLLM, Text Generation Inference, Caikit NLP, InstructLab, FMS HuggingFace Tuning
- **Notebook Environments**: Minimal, PyTorch, CUDA, Generic Data Science, TrustyAI, ROCm, Code Server
- **AI/ML Frameworks**: TrustyAI Runtime, OpenVINO model serving
- **Distributed Computing**: Ray framework, distributed training utilities
- **Infrastructure Components**: Platform core, model serving, data pipelines
- **Registry Analysis**: Trusted vs community registries with detailed breakdown
- **Security Insights**: Deprecated images, unverified sources, actionable recommendations

### Output Formats
- **Markdown**: Human-readable reports with tables and sections
- **JSON**: Structured data for programmatic access

## Example Output

```markdown
# RHOAI 2.24 / OCP 4.18 Container Image Report

## Summary
- **Total Images**: 104 (44 infrastructure + 60 workload)
- **Registries**: quay.io (100), registry.redhat.io (4)
- **Base OS**: RHEL9 (6), Unknown (98)
- **Estimated Size**: ~10.4GB total download
- **Components**: 18 granular functional areas identified

## Granular Component Breakdown
| Component                    | Images | Category            | Description                                    |
|------------------------------|--------|---------------------|------------------------------------------------|
| CUDA Notebooks              | 20     | cuda_notebooks      | GPU-accelerated notebook environments         |
| Minimal Notebooks           | 10     | minimal_notebooks   | Lightweight base notebook environments        |
| PyTorch Notebooks           | 10     | pytorch_notebooks   | PyTorch-optimized notebook environments       |
| Training                     | 8      | training           | Distributed training frameworks               |
| TrustyAI Notebooks          | 8      | trustyai_notebooks | Notebook environments for TrustyAI workflows |
| vLLM                        | 6      | vllm               | High-performance LLM inference engine         |
| Code Server                 | 6      | code_server        | Web-based VS Code development environments    |
| ROCm Notebooks              | 6      | rocm_notebooks     | AMD ROCm-accelerated notebook environments    |
| Ray                         | 4      | ray                | Ray distributed computing framework           |
| InstructLab                 | 2      | instructlab        | Red Hat InstructLab for LLM training        |
| Text Generation Inference   | 2      | text_generation_inference | Optimized text generation inference server |
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
./rhoai_reporter.py --rhoai-version 2.24 --ocp-version 4.18

# Generate granular test report
./rhoai_reporter.py --format json --output test_report.json

# Compare versions for validation
./rhoai_reporter.py --rhoai-version 2.25 --compare-with 2.24

# Query specific components from JSON output
jq '.components[] | select(.category == "vllm")' test_report.json
jq '.components[] | select(.name | contains("TrustyAI"))' test_report.json
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
- ✅ Classify >90% of images correctly with granular component breakdown
- ✅ Identify 18+ specific components (vLLM, TrustyAI, Ray, InstructLab, etc.)
- ✅ Provide actionable security insights with registry trust analysis
- ✅ Support both granular and legacy classification modes
- ✅ Validate feasibility of comprehensive approach

## Key Achievements

**Real-World Validation Results (RHOAI 2.24):**
- **104 images** parsed and classified in <30 seconds
- **18 granular components** identified vs. 3 broad categories previously
- **Specific LLM frameworks** properly separated: vLLM (6), Caikit NLP (2), Text Generation Inference (2)
- **Notebook specializations** clearly categorized: CUDA (20), PyTorch (10), TrustyAI (8), ROCm (6)
- **Distributed computing** components isolated: Ray (4), Training frameworks (8)
- **Security insights** show 96% community registry usage requiring attention