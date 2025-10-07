"""Parsers for OLM catalogs and disconnected helper data."""

import re
from typing import Dict, List

import yaml

from exceptions import DataParsingError
from models import ImageReference, ImageSource


class OLMCatalogParser:
    """Parser for OLM catalog YAML files."""

    def parse_catalog(self, yaml_content: str) -> List[ImageReference]:
        """Extract images from OLM catalog YAML."""
        images = []

        try:
            # Parse multi-document YAML
            documents = list(yaml.safe_load_all(yaml_content))

            for doc in documents:
                if not isinstance(doc, dict):
                    continue

                schema = doc.get('schema', '')

                if schema == 'olm.bundle':
                    # Extract bundle images and related images
                    bundle_images = self._extract_bundle_images(doc)
                    images.extend(bundle_images)

        except yaml.YAMLError as e:
            raise DataParsingError(f"Failed to parse OLM catalog YAML: {e}")
        except Exception as e:
            raise DataParsingError(f"Error processing OLM catalog: {e}")

        return images

    def _extract_bundle_images(self, bundle_data: dict) -> List[ImageReference]:
        """Extract images from a bundle document."""
        images = []

        # Extract main bundle image
        bundle_image = bundle_data.get('image')
        if bundle_image:
            img_ref = ImageReference.from_url(bundle_image, ImageSource.OLM_CATALOG)
            img_ref.semantic_name = bundle_data.get('name', '').replace('rhods-operator.', '')
            img_ref.category = 'bundle'
            images.append(img_ref)

        # Extract related images
        related_images = bundle_data.get('relatedImages', [])
        for related in related_images:
            if isinstance(related, dict):
                image_url = related.get('image')
                if image_url:
                    img_ref = ImageReference.from_url(image_url, ImageSource.OLM_CATALOG)
                    img_ref.semantic_name = related.get('name', '')
                    img_ref.category = 'related'
                    images.append(img_ref)

        return images


class DisconnectedHelperParser:
    """Parser for disconnected helper markdown files."""

    def parse_markdown(self, md_content: str) -> List[ImageReference]:
        """Extract images from markdown lists."""
        images = []

        try:
            # Extract image categories and their images
            categories = self._categorize_images(md_content)

            for category, image_list in categories.items():
                for image_url in image_list:
                    img_ref = ImageReference.from_url(image_url, ImageSource.DISCONNECTED_HELPER)
                    img_ref.category = category
                    images.append(img_ref)

        except Exception as e:
            raise DataParsingError(f"Error processing disconnected helper markdown: {e}")

        return images

    def _categorize_images(self, content: str) -> Dict[str, List[str]]:
        """Group images by category from markdown content."""
        categories = {}
        current_category = "general"

        lines = content.split('\n')

        for line in lines:
            line = line.strip()

            # Detect category headers
            if line.startswith('##') and not line.startswith('###'):
                # Extract category name
                category = line.replace('##', '').strip().lower()
                category = re.sub(r'[^a-z0-9_]', '_', category)
                current_category = category
                if current_category not in categories:
                    categories[current_category] = []

            # Extract image references
            elif line.startswith('- ') and '@sha256:' in line:
                # Extract image URL from markdown list item
                image_match = re.search(r'([a-zA-Z0-9.-]+(?:\:[0-9]+)?/[a-zA-Z0-9._/-]+@sha256:[a-f0-9]{64})', line)
                if image_match:
                    image_url = image_match.group(1)
                    if current_category not in categories:
                        categories[current_category] = []
                    categories[current_category].append(image_url)

            # Also check for images in YAML sections
            elif 'name:' in line and '@sha256:' in line:
                image_match = re.search(r'([a-zA-Z0-9.-]+(?:\:[0-9]+)?/[a-zA-Z0-9._/-]+@sha256:[a-f0-9]{64})', line)
                if image_match:
                    image_url = image_match.group(1)
                    if current_category not in categories:
                        categories[current_category] = []
                    categories[current_category].append(image_url)

        return categories