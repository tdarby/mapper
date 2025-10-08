#!/usr/bin/env python3
"""RHOAI Container Image Reporter - Main CLI application."""

import os
import sys
from pathlib import Path
from typing import Optional

import click
import yaml
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add src directory to path for imports
src_path = str(Path(__file__).parent / "src")
sys.path.insert(0, src_path)

# Import with absolute imports
import analyzer
import exceptions
import github_client
import parsers
import reporter

ImageAnalyzer = analyzer.ImageAnalyzer
RHOAIReporterError = exceptions.RHOAIReporterError
VersionNotFoundError = exceptions.VersionNotFoundError
GitHubAPIClient = github_client.GitHubAPIClient
DisconnectedHelperParser = parsers.DisconnectedHelperParser
OLMCatalogParser = parsers.OLMCatalogParser
ReportGenerator = reporter.ReportGenerator

console = Console()


class RHOAIReporter:
    """Main RHOAI container image reporter application."""

    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.github_client = GitHubAPIClient()
        self.olm_parser = OLMCatalogParser()
        self.markdown_parser = DisconnectedHelperParser()
        self.analyzer = ImageAnalyzer()
        self.reporter = ReportGenerator()

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            console.print(f"[yellow]Warning: Config file {config_path} not found, using defaults[/yellow]")
            return {
                'repositories': {
                    'build_config': 'red-hat-data-services/RHOAI-Build-Config',
                    'disconnected_helper': 'red-hat-data-services/rhoai-disconnected-install-helper'
                },
                'defaults': {
                    'output_format': 'markdown',
                    'include_security_analysis': True
                }
            }

    def generate_report(self, rhoai_version: Optional[str] = None,
                       ocp_version: Optional[str] = None,
                       compare_with: Optional[str] = None,
                       output_format: str = "markdown",
                       output_file: Optional[str] = None,
                       granular: bool = True,
                       show_variants: bool = True) -> None:
        """Generate RHOAI container image report."""

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:

            # Determine versions
            if not rhoai_version or not ocp_version:
                task = progress.add_task("Determining latest versions...", total=None)
                try:
                    latest_rhoai, latest_ocp = self.github_client.get_latest_versions()
                    rhoai_version = rhoai_version or latest_rhoai
                    ocp_version = ocp_version or latest_ocp
                    progress.update(task, description=f"Using RHOAI {rhoai_version} / OCP {ocp_version}")
                except Exception as e:
                    progress.stop()
                    console.print(f"[red]Error determining versions: {e}[/red]")
                    return

            # Fetch OLM catalog data
            task = progress.add_task("Fetching OLM catalog data...", total=None)
            try:
                olm_content = self.github_client.get_olm_catalog(rhoai_version, ocp_version)
                progress.update(task, description="OLM catalog data fetched")
            except Exception as e:
                progress.stop()
                console.print(f"[red]Error fetching OLM catalog: {e}[/red]")
                return

            # Fetch disconnected helper data
            task = progress.add_task("Fetching disconnected helper data...", total=None)
            try:
                helper_content = self.github_client.get_disconnected_helper(rhoai_version)
                progress.update(task, description="Disconnected helper data fetched")
            except Exception as e:
                progress.stop()
                console.print(f"[yellow]Warning: Could not fetch disconnected helper data: {e}[/yellow]")
                helper_content = ""

            # Parse data
            task = progress.add_task("Parsing image data...", total=None)
            try:
                olm_images = self.olm_parser.parse_catalog(olm_content)
                helper_images = []
                if helper_content:
                    helper_images = self.markdown_parser.parse_markdown(helper_content)

                all_images = olm_images + helper_images
                progress.update(task, description=f"Parsed {len(all_images)} images")

                if not all_images:
                    progress.stop()
                    console.print("[yellow]No images found in the specified version[/yellow]")
                    return

            except Exception as e:
                progress.stop()
                console.print(f"[red]Error parsing data: {e}[/red]")
                return

            # Analyze images
            task = progress.add_task("Analyzing images...", total=None)
            try:
                analysis = self.analyzer.analyze_images(all_images, rhoai_version, ocp_version)
                progress.update(task, description="Analysis complete")
            except Exception as e:
                progress.stop()
                console.print(f"[red]Error analyzing images: {e}[/red]")
                return

            # Generate comparison if requested
            if compare_with:
                task = progress.add_task(f"Comparing with version {compare_with}...", total=None)
                try:
                    # Fetch comparison data (simplified for now)
                    comparison_olm = self.github_client.get_olm_catalog(compare_with, ocp_version)
                    comparison_helper = ""
                    try:
                        comparison_helper = self.github_client.get_disconnected_helper(compare_with)
                    except:
                        pass

                    comparison_images = (self.olm_parser.parse_catalog(comparison_olm) +
                                       (self.markdown_parser.parse_markdown(comparison_helper) if comparison_helper else []))

                    analysis.comparison = self.analyzer.compare_versions(all_images, comparison_images)
                    progress.update(task, description=f"Comparison with {compare_with} complete")
                except Exception as e:
                    progress.update(task, description=f"Comparison failed: {e}")

            # Generate report
            task = progress.add_task("Generating report...", total=None)
            try:
                report = self.reporter.generate_report(analysis, output_format)
                progress.update(task, description="Report generated")
            except Exception as e:
                progress.stop()
                console.print(f"[red]Error generating report: {e}[/red]")
                return

        # Output report
        if output_file:
            try:
                with open(output_file, 'w') as f:
                    if output_format == "json":
                        f.write(report.summary)
                    else:
                        f.write(report.summary + "\n" + report.detailed_breakdown + "\n" + report.security_report)
                console.print(f"[green]Report saved to {output_file}[/green]")
            except Exception as e:
                console.print(f"[red]Error saving report: {e}[/red]")
        else:
            # Print to console
            if output_format == "json":
                console.print(report.summary)
            else:
                console.print(report.summary)
                console.print(report.detailed_breakdown)
                console.print(report.security_report)


@click.command()
@click.option('--rhoai-version', help='RHOAI version (e.g., 2.25)')
@click.option('--ocp-version', help='OpenShift Container Platform version (e.g., 4.20)')
@click.option('--compare-with', help='Compare with another RHOAI version')
@click.option('--format', 'output_format', default='markdown', type=click.Choice(['markdown', 'json']),
              help='Output format')
@click.option('--output', 'output_file', help='Output file path')
@click.option('--config', 'config_path', default='config.yaml', help='Configuration file path')
@click.option('--granular/--no-granular', default=True, help='Use granular component classification (default: True)')
@click.option('--show-variants/--no-show-variants', default=True, help='Show detailed variant analysis (default: True)')
def main(rhoai_version: Optional[str], ocp_version: Optional[str], compare_with: Optional[str],
         output_format: str, output_file: Optional[str], config_path: str, granular: bool, show_variants: bool):
    """RHOAI Container Image Reporter - Generate reports for RHOAI/OCP version combinations."""

    console.print("[bold blue]RHOAI Container Image Reporter[/bold blue]")

    try:
        reporter = RHOAIReporter(config_path)
        reporter.generate_report(
            rhoai_version=rhoai_version,
            ocp_version=ocp_version,
            compare_with=compare_with,
            output_format=output_format,
            output_file=output_file,
            granular=granular,
            show_variants=show_variants
        )
    except RHOAIReporterError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()