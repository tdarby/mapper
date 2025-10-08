"""Data models for RHOAI container image analysis."""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum


class ImageSource(Enum):
    """Source of image data."""
    OLM_CATALOG = "olm_catalog"
    DISCONNECTED_HELPER = "disconnected_helper"


class ImageClassification(Enum):
    """Image classification type."""
    INFRASTRUCTURE = "infrastructure"
    WORKLOAD = "workload"
    UNKNOWN = "unknown"


@dataclass
class ImageReference:
    """Container image reference with metadata."""
    image: str
    digest: str
    registry: str
    namespace: str
    repository: str
    tag: Optional[str] = None
    semantic_name: Optional[str] = None
    source: ImageSource = ImageSource.OLM_CATALOG
    classification: ImageClassification = ImageClassification.UNKNOWN
    category: Optional[str] = None
    base_os: Optional[str] = None
    architecture: Optional[str] = None
    python_version: Optional[str] = None
    gpu_support: Optional[str] = None
    variant_type: Optional[str] = None  # workbench, pipeline, notebook, runtime

    @property
    def full_reference(self) -> str:
        """Get full image reference."""
        if self.digest:
            return f"{self.registry}/{self.namespace}/{self.repository}@{self.digest}"
        elif self.tag:
            return f"{self.registry}/{self.namespace}/{self.repository}:{self.tag}"
        else:
            return f"{self.registry}/{self.namespace}/{self.repository}"

    @classmethod
    def from_url(cls, image_url: str, source: ImageSource = ImageSource.OLM_CATALOG) -> 'ImageReference':
        """Parse image URL into components."""
        # Handle different URL formats
        if '@sha256:' in image_url:
            base_url, digest = image_url.split('@')
            tag = None
        elif ':' in image_url and not image_url.startswith('sha256:'):
            # Check if this is a tag or part of registry
            parts = image_url.split(':')
            if len(parts) > 2:  # registry:port/namespace/repo:tag
                base_url = ':'.join(parts[:-1])
                tag = parts[-1]
                digest = None
            else:  # registry/namespace/repo:tag
                base_url, tag = image_url.rsplit(':', 1)
                digest = None
        else:
            base_url = image_url
            tag = None
            digest = None

        # Parse registry/namespace/repository
        url_parts = base_url.split('/')
        if len(url_parts) >= 3:
            registry = url_parts[0]
            namespace = url_parts[1]
            repository = '/'.join(url_parts[2:])
        else:
            registry = "unknown"
            namespace = "unknown"
            repository = base_url

        return cls(
            image=image_url,
            digest=digest,
            registry=registry,
            namespace=namespace,
            repository=repository,
            tag=tag,
            source=source
        )


@dataclass
class ImageVariant:
    """Represents different variants of the same base image."""
    base_name: str
    digest: str
    sources: List[ImageSource]
    architecture: Optional[str] = None
    python_version: Optional[str] = None
    gpu_support: Optional[str] = None
    base_os: Optional[str] = None
    variant_type: Optional[str] = None
    reference_count: int = 1

@dataclass
class ComponentInfo:
    """Information about a component and its images."""
    name: str
    images: List[ImageReference]
    category: str
    description: Optional[str] = None
    upstream_repo: Optional[str] = None
    unique_digests: int = 0
    total_references: int = 0
    variants: List[ImageVariant] = None


@dataclass
class RegistryAnalysis:
    """Analysis of image distribution by registry."""
    registry_counts: Dict[str, int]
    namespace_counts: Dict[str, int]
    total_images: int


@dataclass
class SecurityInsights:
    """Security analysis results."""
    trusted_registries: int
    community_registries: int
    deprecated_images: List[str]
    unverified_sources: List[str]
    recommendations: List[str]


@dataclass
class VersionComparison:
    """Comparison between two versions."""
    added_images: List[ImageReference]
    removed_images: List[ImageReference]
    updated_images: List[ImageReference]
    unchanged_images: List[ImageReference]


@dataclass
class Analysis:
    """Complete analysis results."""
    rhoai_version: str
    ocp_version: str
    total_images: int
    infrastructure_images: List[ImageReference]
    workload_images: List[ImageReference]
    components: List[ComponentInfo]
    registry_analysis: RegistryAnalysis
    security_insights: SecurityInsights
    comparison: Optional[VersionComparison] = None


@dataclass
class Report:
    """Generated report data."""
    analysis: Analysis
    summary: str
    detailed_breakdown: str
    security_report: str
    format: str = "markdown"