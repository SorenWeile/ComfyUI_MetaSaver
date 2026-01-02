"""
ComfyUI MetaSaver - Custom Image Save Node with Metadata
Author: Your Name
License: MIT

A ComfyUI custom node that allows saving images with custom metadata fields.
Users can dynamically specify how many metadata fields to add and give them custom names.
"""

from .meta_saver_node import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
