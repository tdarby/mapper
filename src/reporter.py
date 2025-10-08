"""Report generation system for RHOAI container image analysis."""

import json
from typing import Dict, List

try:
    from tabulate import tabulate
    TABULATE_AVAILABLE = True
except ImportError:
    TABULATE_AVAILABLE = False
    def tabulate(data, headers=None, tablefmt="pipe"):
        """Fallback tabulate implementation"""
        if not headers:
            return "\n".join([" | ".join(map(str, row)) for row in data])

        result = " | ".join(headers) + "\n"
        result += " | ".join(["---"] * len(headers)) + "\n"
        result += "\n".join([" | ".join(map(str, row)) for row in data])
        return result

from models import Analysis, ComponentInfo, Report


class ReportGenerator:
    """Generates human-readable reports from analysis data."""

    def generate_report(self, analysis: Analysis, format: str = "markdown") -> Report:
        """Generate complete report from analysis."""
        if format == "json":
            return self._generate_json_report(analysis)
        else:
            return self._generate_markdown_report(analysis)

    def _generate_markdown_report(self, analysis: Analysis) -> Report:
        """Generate markdown-formatted report."""
        summary = self._generate_summary_report(analysis)
        detailed = self._generate_detailed_report(analysis)
        security = self._generate_security_report(analysis)

        return Report(
            analysis=analysis,
            summary=summary,
            detailed_breakdown=detailed,
            security_report=security,
            format="markdown"
        )

    def _generate_json_report(self, analysis: Analysis) -> Report:
        """Generate JSON-formatted report."""
        report_data = {
            "rhoai_version": analysis.rhoai_version,
            "ocp_version": analysis.ocp_version,
            "summary": {
                "total_images": analysis.total_images,
                "infrastructure_images": len(analysis.infrastructure_images),
                "workload_images": len(analysis.workload_images),
                "registries": analysis.registry_analysis.registry_counts,
                "components": len(analysis.components)
            },
            "components": [
                {
                    "name": comp.name,
                    "category": comp.category,
                    "image_count": len(comp.images),
                    "unique_digests": comp.unique_digests,
                    "total_references": comp.total_references,
                    "description": comp.description,
                    "variants": [
                        {
                            "base_name": variant.base_name,
                            "digest": variant.digest[:12] + "...",  # Truncated for readability
                            "sources": [source.value for source in variant.sources],
                            "architecture": variant.architecture,
                            "python_version": variant.python_version,
                            "gpu_support": variant.gpu_support,
                            "base_os": variant.base_os,
                            "variant_type": variant.variant_type,
                            "reference_count": variant.reference_count
                        }
                        for variant in (comp.variants or [])
                    ],
                    "images": [img.full_reference for img in comp.images]
                }
                for comp in analysis.components
            ],
            "security": {
                "trusted_registries": analysis.security_insights.trusted_registries,
                "community_registries": analysis.security_insights.community_registries,
                "recommendations": analysis.security_insights.recommendations
            }
        }

        json_content = json.dumps(report_data, indent=2)

        return Report(
            analysis=analysis,
            summary=json_content,
            detailed_breakdown=json_content,
            security_report=json_content,
            format="json"
        )

    def _generate_summary_report(self, analysis: Analysis) -> str:
        """Create executive summary with key metrics."""
        base_os_counts = {}
        for img in analysis.infrastructure_images + analysis.workload_images:
            base_os = img.base_os or "Unknown"
            base_os_counts[base_os] = base_os_counts.get(base_os, 0) + 1

        base_os_summary = ", ".join([f"{os} ({count})" for os, count in base_os_counts.items()])

        # Calculate estimated total size (rough estimate)
        estimated_size_gb = analysis.total_images * 0.1  # Assume 100MB average per image

        summary = f"""# RHOAI {analysis.rhoai_version} / OCP {analysis.ocp_version} Container Image Report

## Summary
- **Total Images**: {analysis.total_images} ({len(analysis.infrastructure_images)} infrastructure + {len(analysis.workload_images)} workload)
- **Registries**: {', '.join([f"{reg} ({count})" for reg, count in analysis.registry_analysis.registry_counts.items()])}
- **Base OS**: {base_os_summary}
- **Estimated Size**: ~{estimated_size_gb:.1f}GB total download
- **Components**: {len(analysis.components)} functional areas identified

## Component Overview
"""

        # Add enhanced component summary table
        component_data = []
        for comp in sorted(analysis.components, key=lambda x: len(x.images), reverse=True):
            # Create variant summary
            variant_info = ""
            if comp.variants and len(comp.variants) > 1:
                variant_details = []
                for variant in comp.variants[:3]:  # Show top 3 variants
                    details = []
                    if variant.python_version:
                        details.append(f"Py{variant.python_version}")
                    if variant.gpu_support and variant.gpu_support != 'CPU':
                        details.append(variant.gpu_support)
                    if variant.base_os and variant.base_os != 'Unknown':
                        details.append(variant.base_os)
                    if variant.variant_type and variant.variant_type != 'base':
                        details.append(variant.variant_type)

                    if details:
                        variant_details.append(f"[{', '.join(details)}]")

                if variant_details:
                    variant_info = f" | Variants: {', '.join(variant_details)}"
                    if len(comp.variants) > 3:
                        variant_info += f" (+{len(comp.variants) - 3} more)"

            component_data.append([
                comp.name,
                f"{len(comp.images)} ({comp.unique_digests} unique)",
                comp.category.replace('_', ' ').title(),
                (comp.description[:40] + "..." if comp.description and len(comp.description) > 40 else comp.description or "") + variant_info
            ])

        component_table = tabulate(
            component_data,
            headers=["Component", "Images (Unique)", "Type", "Description & Variants"],
            tablefmt="pipe"
        )

        summary += component_table

        # Add key changes if comparison available
        if analysis.comparison:
            summary += f"""

## Key Changes
- **Added**: {len(analysis.comparison.added_images)} new images
- **Removed**: {len(analysis.comparison.removed_images)} deprecated images
- **Unchanged**: {len(analysis.comparison.unchanged_images)} existing images
"""

        return summary

    def _generate_detailed_report(self, analysis: Analysis) -> str:
        """Full breakdown by component and category."""
        detailed = f"""
## Detailed Component Breakdown

### Infrastructure Components ({len(analysis.infrastructure_images)} images)

"""

        # Group infrastructure components
        infra_components = [comp for comp in analysis.components
                          if any(img.classification.value == "infrastructure" for img in comp.images)]

        for comp in sorted(infra_components, key=lambda x: len(x.images), reverse=True):
            infra_images = [img for img in comp.images if img.classification.value == "infrastructure"]
            if infra_images:
                detailed += f"#### {comp.name} ({len(infra_images)} images, {comp.unique_digests} unique)\n"
                detailed += f"*{comp.description}*\n\n"

                # Show variant breakdown if applicable
                if comp.variants and len(comp.variants) > 1:
                    detailed += "**Build Variants:**\n"
                    for variant in comp.variants:
                        variant_details = []
                        if variant.python_version:
                            variant_details.append(f"Python {variant.python_version}")
                        if variant.gpu_support and variant.gpu_support != 'CPU':
                            variant_details.append(variant.gpu_support)
                        if variant.base_os and variant.base_os != 'Unknown':
                            variant_details.append(variant.base_os)
                        if variant.variant_type and variant.variant_type != 'base':
                            variant_details.append(variant.variant_type.title())

                        detail_str = f" ({', '.join(variant_details)})" if variant_details else ""
                        sources_str = f" [Sources: {', '.join(s.value for s in variant.sources)}]"
                        detailed += f"- `{variant.digest[:12]}...`{detail_str}{sources_str}\n"
                    detailed += "\n"

                # Show sample images
                for img in infra_images[:3]:  # Show first 3 images
                    semantic_name = f" ({img.semantic_name})" if img.semantic_name else ""
                    detailed += f"- {img.full_reference}{semantic_name}\n"

                if len(infra_images) > 3:
                    detailed += f"- ... and {len(infra_images) - 3} more images\n"

                detailed += "\n"

        detailed += f"""
### Workload Components ({len(analysis.workload_images)} images)

"""

        # Group workload components
        workload_components = [comp for comp in analysis.components
                             if any(img.classification.value == "workload" for img in comp.images)]

        for comp in sorted(workload_components, key=lambda x: len(x.images), reverse=True):
            workload_images = [img for img in comp.images if img.classification.value == "workload"]
            if workload_images:
                detailed += f"#### {comp.name} ({len(workload_images)} images, {comp.unique_digests} unique)\n"
                detailed += f"*{comp.description}*\n\n"

                # Show variant breakdown if applicable
                if comp.variants and len(comp.variants) > 1:
                    detailed += "**Build Variants:**\n"
                    for variant in comp.variants:
                        variant_details = []
                        if variant.python_version:
                            variant_details.append(f"Python {variant.python_version}")
                        if variant.gpu_support and variant.gpu_support != 'CPU':
                            variant_details.append(variant.gpu_support)
                        if variant.base_os and variant.base_os != 'Unknown':
                            variant_details.append(variant.base_os)
                        if variant.variant_type and variant.variant_type != 'base':
                            variant_details.append(variant.variant_type.title())
                        if variant.architecture and variant.architecture != 'amd64':
                            variant_details.append(variant.architecture)

                        detail_str = f" ({', '.join(variant_details)})" if variant_details else ""
                        sources_str = f" [Sources: {', '.join(s.value for s in variant.sources)}]"
                        refs_str = f" ({variant.reference_count} refs)" if variant.reference_count > 1 else ""
                        detailed += f"- `{variant.digest[:12]}...`{detail_str}{sources_str}{refs_str}\n"
                    detailed += "\n"

                # Show sample images (fewer for workload due to typically more images)
                for img in workload_images[:2]:
                    detailed += f"- {img.full_reference}\n"

                if len(workload_images) > 2:
                    detailed += f"- ... and {len(workload_images) - 2} more images\n"

                detailed += "\n"

        return detailed

    def _generate_security_report(self, analysis: Analysis) -> str:
        """Security-focused analysis."""
        security = f"""
## Security Analysis

### Registry Distribution
- **Trusted Red Hat**: {analysis.security_insights.trusted_registries} images ({analysis.security_insights.trusted_registries/analysis.total_images*100:.1f}%)
- **Community/Other**: {analysis.security_insights.community_registries} images ({analysis.security_insights.community_registries/analysis.total_images*100:.1f}%)

### Registry Breakdown
"""

        # Registry details table
        registry_data = []
        for registry, count in sorted(analysis.registry_analysis.registry_counts.items(), key=lambda x: x[1], reverse=True):
            trust_level = "Trusted" if registry in ["registry.redhat.io", "registry.access.redhat.com"] else "Community"
            percentage = (count / analysis.total_images) * 100
            registry_data.append([registry, count, f"{percentage:.1f}%", trust_level])

        registry_table = tabulate(
            registry_data,
            headers=["Registry", "Images", "Percentage", "Trust Level"],
            tablefmt="pipe"
        )

        security += registry_table

        # Security concerns
        if analysis.security_insights.deprecated_images:
            security += f"""

### Potential Concerns
- **Deprecated Images**: {len(analysis.security_insights.deprecated_images)} images using deprecated patterns
"""
            for img in analysis.security_insights.deprecated_images[:5]:
                security += f"  - {img}\n"

        if analysis.security_insights.unverified_sources:
            security += f"""
- **Unverified Sources**: {len(analysis.security_insights.unverified_sources)} images from non-standard registries
"""
            for img in analysis.security_insights.unverified_sources[:5]:
                security += f"  - {img}\n"

        # Recommendations
        if analysis.security_insights.recommendations:
            security += """

### Recommendations
"""
            for rec in analysis.security_insights.recommendations:
                security += f"- {rec}\n"

        return security