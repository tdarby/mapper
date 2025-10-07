"""Image analysis and classification engine."""

import re
from collections import defaultdict
from typing import Dict, List

from models import (
    Analysis, ComponentInfo, ImageClassification, ImageReference,
    RegistryAnalysis, SecurityInsights, VersionComparison
)


class ImageAnalyzer:
    """Analyzes and classifies container images."""

    def __init__(self):
        # Infrastructure image patterns
        self.infrastructure_patterns = [
            r'.*-operator.*',
            r'.*-controller.*',
            r'.*-server.*',
            r'.*-proxy.*',
            r'.*-bundle.*',
            r'odh-.*',
            r'.*modelmesh.*',
            r'.*kuberay.*',
            r'.*codeflare.*',
            r'.*pipelines.*'
        ]

        # Workload image patterns
        self.workload_patterns = [
            r'.*-notebook.*',
            r'.*-workbench.*',
            r'.*code-server.*',
            r'.*jupyter.*',
            r'.*tensorflow.*',
            r'.*pytorch.*',
            r'.*cuda.*',
            r'.*training.*'
        ]

        # Trusted registries
        self.trusted_registries = [
            'registry.redhat.io',
            'registry.access.redhat.com'
        ]

        # Component mapping patterns
        self.component_patterns = {
            'platform_core': [r'odh-operator', r'odh-dashboard', r'odh-deployer'],
            'notebook_management': [r'odh-notebook-controller', r'kf-notebook-controller'],
            'model_serving': [r'modelmesh', r'kserve', r'model-controller'],
            'data_pipelines': [r'ml-pipelines', r'data-science-pipelines', r'argo'],
            'distributed_computing': [r'kuberay', r'codeflare', r'training-operator'],
            'development_environments': [r'notebook', r'workbench', r'code-server'],
            'ml_runtimes': [r'tensorflow', r'pytorch', r'cuda'],
            'specialized_ai': [r'openvino', r'trustyai']
        }

    def analyze_images(self, images: List[ImageReference], rhoai_version: str, ocp_version: str) -> Analysis:
        """Perform complete analysis of images."""
        # Classify images
        self._classify_images(images)

        # Detect base OS
        self._detect_base_os(images)

        # Separate by classification
        infrastructure_images = [img for img in images if img.classification == ImageClassification.INFRASTRUCTURE]
        workload_images = [img for img in images if img.classification == ImageClassification.WORKLOAD]

        # Group into components
        components = self._group_into_components(images)

        # Analyze registries
        registry_analysis = self._analyze_registries(images)

        # Security insights
        security_insights = self._analyze_security(images)

        return Analysis(
            rhoai_version=rhoai_version,
            ocp_version=ocp_version,
            total_images=len(images),
            infrastructure_images=infrastructure_images,
            workload_images=workload_images,
            components=components,
            registry_analysis=registry_analysis,
            security_insights=security_insights
        )

    def _classify_images(self, images: List[ImageReference]) -> None:
        """Classify images as infrastructure or workload."""
        for image in images:
            image_name = image.repository.lower()

            # Check infrastructure patterns
            if any(re.match(pattern, image_name) for pattern in self.infrastructure_patterns):
                image.classification = ImageClassification.INFRASTRUCTURE
            # Check workload patterns
            elif any(re.match(pattern, image_name) for pattern in self.workload_patterns):
                image.classification = ImageClassification.WORKLOAD
            # Default classification based on registry and source
            elif image.registry in self.trusted_registries:
                image.classification = ImageClassification.INFRASTRUCTURE
            else:
                image.classification = ImageClassification.WORKLOAD

    def _detect_base_os(self, images: List[ImageReference]) -> None:
        """Detect base OS from image names."""
        for image in images:
            image_name = image.repository.lower()
            if '-rhel8' in image_name or 'rhel8' in image_name:
                image.base_os = 'RHEL8'
            elif '-rhel9' in image_name or 'rhel9' in image_name:
                image.base_os = 'RHEL9'
            elif '-ubi' in image_name or 'ubi' in image_name:
                image.base_os = 'UBI'
            else:
                image.base_os = 'Unknown'

    def _group_into_components(self, images: List[ImageReference]) -> List[ComponentInfo]:
        """Group images into functional components."""
        components = []
        component_groups = defaultdict(list)

        # Group images by component patterns
        for image in images:
            image_name = image.repository.lower()
            assigned = False

            for component_type, patterns in self.component_patterns.items():
                if any(pattern in image_name for pattern in patterns):
                    component_groups[component_type].append(image)
                    assigned = True
                    break

            if not assigned:
                component_groups['other'].append(image)

        # Create ComponentInfo objects
        for component_type, img_list in component_groups.items():
            if img_list:
                components.append(ComponentInfo(
                    name=component_type.replace('_', ' ').title(),
                    images=img_list,
                    category=component_type,
                    description=self._get_component_description(component_type)
                ))

        return components

    def _get_component_description(self, component_type: str) -> str:
        """Get description for component type."""
        descriptions = {
            'platform_core': 'Core platform services and user interface',
            'notebook_management': 'Interactive development environment management',
            'model_serving': 'ML model deployment and inference',
            'data_pipelines': 'Workflow orchestration and data processing',
            'distributed_computing': 'Distributed ML training and batch processing',
            'development_environments': 'Interactive development and experimentation',
            'ml_runtimes': 'Model training and development environments',
            'specialized_ai': 'Specialized model execution and analysis',
            'other': 'Other components'
        }
        return descriptions.get(component_type, 'Unknown component type')

    def _analyze_registries(self, images: List[ImageReference]) -> RegistryAnalysis:
        """Analyze image distribution by registry."""
        registry_counts = defaultdict(int)
        namespace_counts = defaultdict(int)

        for image in images:
            registry_counts[image.registry] += 1
            namespace_key = f"{image.registry}/{image.namespace}"
            namespace_counts[namespace_key] += 1

        return RegistryAnalysis(
            registry_counts=dict(registry_counts),
            namespace_counts=dict(namespace_counts),
            total_images=len(images)
        )

    def _analyze_security(self, images: List[ImageReference]) -> SecurityInsights:
        """Perform security analysis on images."""
        trusted_count = 0
        community_count = 0
        deprecated_images = []
        unverified_sources = []
        recommendations = []

        for image in images:
            if image.registry in self.trusted_registries:
                trusted_count += 1
            else:
                community_count += 1

            # Check for deprecated patterns
            if any(pattern in image.repository.lower() for pattern in ['deprecated', 'legacy', 'old']):
                deprecated_images.append(image.full_reference)

            # Check for potentially unverified sources
            if image.registry not in self.trusted_registries and 'quay.io' not in image.registry:
                unverified_sources.append(image.full_reference)

        # Generate recommendations
        if deprecated_images:
            recommendations.append(f"Migrate {len(deprecated_images)} deprecated images before next release")

        if unverified_sources:
            recommendations.append(f"Verify {len(unverified_sources)} images from non-standard registries")

        if community_count > trusted_count:
            recommendations.append("Consider migrating community images to trusted registries")

        return SecurityInsights(
            trusted_registries=trusted_count,
            community_registries=community_count,
            deprecated_images=deprecated_images,
            unverified_sources=unverified_sources,
            recommendations=recommendations
        )

    def compare_versions(self, current_images: List[ImageReference],
                        previous_images: List[ImageReference]) -> VersionComparison:
        """Compare two sets of images to identify changes."""
        current_digests = {img.digest: img for img in current_images if img.digest}
        previous_digests = {img.digest: img for img in previous_images if img.digest}

        # Find added images
        added_images = [img for digest, img in current_digests.items()
                       if digest not in previous_digests]

        # Find removed images
        removed_images = [img for digest, img in previous_digests.items()
                         if digest not in current_digests]

        # Find unchanged images
        unchanged_images = [img for digest, img in current_digests.items()
                          if digest in previous_digests]

        # For now, assume no updated images (same component, different digest)
        # This would require more sophisticated component matching
        updated_images = []

        return VersionComparison(
            added_images=added_images,
            removed_images=removed_images,
            updated_images=updated_images,
            unchanged_images=unchanged_images
        )