import os
import json
import numpy as np
from PIL import Image, PngImagePlugin
from PIL.PngImagePlugin import PngInfo
import folder_paths


class MetaSaverNode:
    """
    A ComfyUI custom node that saves images with custom metadata fields.
    Allows dynamic specification of metadata fields with custom names.
    """

    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 4

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
                "num_metadata_fields": ("INT", {"default": 3, "min": 0, "max": 20, "step": 1}),
            },
            "optional": {
                # Dynamic metadata fields will be added via RETURN_TYPES
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO"
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "image"

    def save_images(self, images, filename_prefix="ComfyUI", num_metadata_fields=3,
                    prompt=None, extra_pnginfo=None, **kwargs):
        """
        Save images with custom metadata embedded in PNG files.

        Args:
            images: Tensor of images to save
            filename_prefix: Prefix for saved filenames
            num_metadata_fields: Number of custom metadata fields (configured in UI)
            prompt: ComfyUI workflow prompt (auto-injected)
            extra_pnginfo: Extra PNG info (auto-injected)
            **kwargs: Dynamic metadata fields (meta_field_0, meta_field_1, etc.)
        """
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = \
            folder_paths.get_save_image_path(filename_prefix, self.output_dir,
                                            images[0].shape[1], images[0].shape[0])

        results = list()

        # Collect custom metadata from kwargs
        custom_metadata = {}
        for i in range(num_metadata_fields):
            field_name_key = f"meta_name_{i}"
            field_value_key = f"meta_value_{i}"

            if field_name_key in kwargs and field_value_key in kwargs:
                field_name = kwargs[field_name_key]
                field_value = kwargs[field_value_key]

                # Only add if both name and value are provided
                if field_name and field_name.strip():
                    custom_metadata[field_name] = self._format_value(field_value)

        for (batch_number, image) in enumerate(images):
            # Convert tensor to PIL Image
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

            # Prepare PNG metadata
            metadata = PngInfo()

            # Add ComfyUI workflow metadata (standard)
            if prompt is not None:
                metadata.add_text("prompt", json.dumps(prompt))
            if extra_pnginfo is not None:
                for key, value in extra_pnginfo.items():
                    metadata.add_text(key, json.dumps(value))

            # Add custom metadata
            if custom_metadata:
                metadata.add_text("custom_metadata", json.dumps(custom_metadata))

                # Also add individual fields for easier reading
                for key, value in custom_metadata.items():
                    metadata.add_text(key, str(value))

            # Generate filename
            file = f"{filename}_{counter:05}_.png"
            img.save(os.path.join(full_output_folder, file),
                    pnginfo=metadata,
                    compress_level=self.compress_level)

            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
            })

            counter += 1

        return {"ui": {"images": results}}

    def _format_value(self, value):
        """Format values for JSON serialization."""
        if isinstance(value, (int, float, str, bool)):
            return value
        elif isinstance(value, (list, tuple)):
            # Handle arrays (like seeds from multiple samplers)
            return list(value)
        else:
            # Convert to string as fallback
            return str(value)


class MetaSaverDynamicNode:
    """
    Advanced version with truly dynamic inputs based on num_metadata_fields.
    This version regenerates inputs when num_metadata_fields changes.
    """

    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 4

    @classmethod
    def INPUT_TYPES(cls):
        # Note: This is the base configuration. Dynamic inputs are handled by ComfyUI
        # when it detects the IS_CHANGED method
        return {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
                "num_metadata_fields": ("INT", {"default": 3, "min": 0, "max": 20, "step": 1}),
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO"
            },
        }

    @classmethod
    def VALIDATE_INPUTS(cls, num_metadata_fields, **kwargs):
        """Validate that metadata field names are provided."""
        if num_metadata_fields < 0 or num_metadata_fields > 20:
            return "num_metadata_fields must be between 0 and 20"
        return True

    RETURN_TYPES = ()
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "image"

    def save_images(self, images, filename_prefix="ComfyUI", num_metadata_fields=3,
                    prompt=None, extra_pnginfo=None, **kwargs):
        """
        Save images with custom metadata embedded in PNG files.

        Args:
            images: Tensor of images to save
            filename_prefix: Prefix for saved filenames
            num_metadata_fields: Number of custom metadata fields (configured in UI)
            prompt: ComfyUI workflow prompt (auto-injected)
            extra_pnginfo: Extra PNG info (auto-injected)
            **kwargs: Dynamic metadata fields (meta_name_0, meta_value_0, etc.)
        """
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = \
            folder_paths.get_save_image_path(filename_prefix, self.output_dir,
                                            images[0].shape[1], images[0].shape[0])

        results = list()

        # Collect custom metadata from kwargs
        custom_metadata = {}
        for i in range(num_metadata_fields):
            field_name_key = f"meta_name_{i}"
            field_value_key = f"meta_value_{i}"

            if field_name_key in kwargs and field_value_key in kwargs:
                field_name = kwargs[field_name_key]
                field_value = kwargs[field_value_key]

                # Only add if both name and value are provided
                if field_name and field_name.strip():
                    custom_metadata[field_name] = self._format_value(field_value)

        for (batch_number, image) in enumerate(images):
            # Convert tensor to PIL Image
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

            # Prepare PNG metadata
            metadata = PngInfo()

            # Add ComfyUI workflow metadata (standard)
            if prompt is not None:
                metadata.add_text("prompt", json.dumps(prompt))
            if extra_pnginfo is not None:
                for key, value in extra_pnginfo.items():
                    metadata.add_text(key, json.dumps(value))

            # Add custom metadata as structured JSON
            if custom_metadata:
                metadata.add_text("custom_metadata", json.dumps(custom_metadata, indent=2))

                # Also add individual fields for easier external reading
                for key, value in custom_metadata.items():
                    metadata.add_text(f"meta_{key}", str(value))

            # Generate filename
            file = f"{filename}_{counter:05}_.png"
            img.save(os.path.join(full_output_folder, file),
                    pnginfo=metadata,
                    compress_level=self.compress_level)

            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
            })

            counter += 1

        return {"ui": {"images": results}}

    def _format_value(self, value):
        """Format values for JSON serialization."""
        if isinstance(value, (int, float, str, bool)):
            return value
        elif isinstance(value, (list, tuple)):
            # Handle arrays (like seeds from multiple samplers)
            return list(value)
        elif hasattr(value, 'item'):  # numpy types
            return value.item()
        else:
            # Convert to string as fallback
            return str(value)


# Node registration
NODE_CLASS_MAPPINGS = {
    "MetaSaver": MetaSaverNode,
    "MetaSaverDynamic": MetaSaverDynamicNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MetaSaver": "Save Image with Custom Metadata",
    "MetaSaverDynamic": "Save Image with Custom Metadata (Dynamic)",
}
