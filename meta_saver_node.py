import os
import json
import numpy as np
from PIL import Image, PngImagePlugin
from PIL.PngImagePlugin import PngInfo
import folder_paths

try:
    import av
    import torch
    from fractions import Fraction
    HAS_AV = True
except ImportError:
    HAS_AV = False


class AnyType(str):
    """A special class that is always equal in comparisons. This allows the wildcard to accept any type."""

    def __eq__(self, _) -> bool:
        return True

    def __ne__(self, __value: object) -> bool:
        return False


# Create a wildcard instance for use in INPUT_TYPES
ANY = AnyType("*")


class MetaSaverNode:
    """
    A ComfyUI custom node that saves images with custom metadata fields.
    Uses a fixed number of optional metadata fields (all optional).
    """

    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 4

    @classmethod
    def INPUT_TYPES(cls):
        # Create optional inputs for metadata fields (up to 10 fields)
        # Users can use as many as they need
        optional_inputs = {}
        for i in range(10):
            optional_inputs[f"meta_name_{i}"] = ("STRING", {"default": "", "multiline": False})
            optional_inputs[f"meta_value_{i}"] = (ANY,)

        return {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
            },
            "optional": optional_inputs,
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO"
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "image"

    def save_images(self, images, filename_prefix="ComfyUI",
                    prompt=None, extra_pnginfo=None, **kwargs):
        """
        Save images with custom metadata embedded in PNG files.

        Args:
            images: Tensor of images to save
            filename_prefix: Prefix for saved filenames
            prompt: ComfyUI workflow prompt (auto-injected)
            extra_pnginfo: Extra PNG info (auto-injected)
            **kwargs: Dynamic metadata fields (meta_name_0, meta_value_0, etc.)
        """
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = \
            folder_paths.get_save_image_path(filename_prefix, self.output_dir,
                                            images[0].shape[1], images[0].shape[0])

        results = list()

        # Collect custom metadata from kwargs (check up to 10 fields)
        custom_metadata = {}
        for i in range(10):
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
    Advanced version with even more metadata fields (up to 20).
    All fields are optional - just fill in the ones you need.
    """

    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 4

    @classmethod
    def INPUT_TYPES(cls):
        # Create optional inputs for metadata fields (up to 20 fields)
        optional_inputs = {}
        for i in range(20):
            optional_inputs[f"meta_name_{i}"] = ("STRING", {"default": "", "multiline": False})
            optional_inputs[f"meta_value_{i}"] = (ANY,)

        return {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
            },
            "optional": optional_inputs,
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO"
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "image"

    def save_images(self, images, filename_prefix="ComfyUI",
                    prompt=None, extra_pnginfo=None, **kwargs):
        """
        Save images with custom metadata embedded in PNG files.

        Args:
            images: Tensor of images to save
            filename_prefix: Prefix for saved filenames
            prompt: ComfyUI workflow prompt (auto-injected)
            extra_pnginfo: Extra PNG info (auto-injected)
            **kwargs: Dynamic metadata fields (meta_name_0, meta_value_0, etc.)
        """
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = \
            folder_paths.get_save_image_path(filename_prefix, self.output_dir,
                                            images[0].shape[1], images[0].shape[0])

        results = list()

        # Collect custom metadata from kwargs (check up to 20 fields)
        custom_metadata = {}
        for i in range(20):
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


class MetaVideoSaverNode:
    """
    A ComfyUI custom node that saves video (from image frames) with custom metadata.
    Supports MP4 (H.264) and WEBM (VP9) output formats.
    Uses up to 10 optional custom metadata fields embedded in the video container.
    """

    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""

    @classmethod
    def INPUT_TYPES(cls):
        optional_inputs = {}
        for i in range(10):
            optional_inputs[f"meta_name_{i}"] = ("STRING", {"default": "", "multiline": False})
            optional_inputs[f"meta_value_{i}"] = (ANY,)

        return {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "video/ComfyUI"}),
                "fps": ("FLOAT", {"default": 24.0, "min": 0.01, "max": 1000.0, "step": 0.01}),
                "format": (["mp4", "webm"],),
            },
            "optional": optional_inputs,
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO"
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "save_video"
    OUTPUT_NODE = True
    CATEGORY = "image/video"

    def save_video(self, images, filename_prefix="video/ComfyUI", fps=24.0, format="mp4",
                   prompt=None, extra_pnginfo=None, **kwargs):
        if not HAS_AV:
            raise RuntimeError("PyAV (av) is not installed. Cannot save video.")

        full_output_folder, filename, counter, subfolder, filename_prefix = \
            folder_paths.get_save_image_path(filename_prefix, self.output_dir,
                                             images[0].shape[1], images[0].shape[0])

        # Collect custom metadata
        custom_metadata = {}
        for i in range(10):
            name_key = f"meta_name_{i}"
            val_key = f"meta_value_{i}"
            if name_key in kwargs and val_key in kwargs:
                field_name = kwargs[name_key]
                if field_name and field_name.strip():
                    custom_metadata[field_name] = self._format_value(kwargs[val_key])

        file = f"{filename}_{counter:05}_.{format}"
        output_path = os.path.join(full_output_folder, file)

        open_options = {}
        if format == "mp4":
            open_options = {"movflags": "use_metadata_tags"}

        container = av.open(output_path, mode="w", options=open_options)

        # Embed ComfyUI workflow metadata
        if prompt is not None:
            container.metadata["prompt"] = json.dumps(prompt)
        if extra_pnginfo is not None:
            for key, value in extra_pnginfo.items():
                container.metadata[key] = json.dumps(value)

        # Embed custom metadata
        if custom_metadata:
            container.metadata["custom_metadata"] = json.dumps(custom_metadata)
            for key, value in custom_metadata.items():
                container.metadata[key] = str(value)

        codec_name = "libx264" if format == "mp4" else "libvpx-vp9"
        pix_fmt = "yuv420p"
        stream = container.add_stream(codec_name, rate=Fraction(round(fps * 1000), 1000))
        stream.width = images.shape[-2]
        stream.height = images.shape[-3]
        stream.pix_fmt = pix_fmt
        if format == "webm":
            stream.bit_rate = 0
            stream.options = {"crf": "32"}

        for frame_tensor in images:
            frame_np = torch.clamp(frame_tensor[..., :3] * 255, 0, 255).to(
                device=torch.device("cpu"), dtype=torch.uint8
            ).numpy()
            frame = av.VideoFrame.from_ndarray(frame_np, format="rgb24")
            for packet in stream.encode(frame):
                container.mux(packet)
        container.mux(stream.encode())
        container.close()

        results = [{"filename": file, "subfolder": subfolder, "type": self.type}]
        return {"ui": {"videos": results}}

    def _format_value(self, value):
        if isinstance(value, (int, float, str, bool)):
            return value
        elif isinstance(value, (list, tuple)):
            return list(value)
        elif hasattr(value, "item"):
            return value.item()
        else:
            return str(value)


class MetaVideoSaverDynamicNode:
    """
    Advanced version of MetaVideoSaverNode with up to 20 metadata fields.
    """

    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""

    @classmethod
    def INPUT_TYPES(cls):
        optional_inputs = {}
        for i in range(20):
            optional_inputs[f"meta_name_{i}"] = ("STRING", {"default": "", "multiline": False})
            optional_inputs[f"meta_value_{i}"] = (ANY,)

        return {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "video/ComfyUI"}),
                "fps": ("FLOAT", {"default": 24.0, "min": 0.01, "max": 1000.0, "step": 0.01}),
                "format": (["mp4", "webm"],),
            },
            "optional": optional_inputs,
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO"
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "save_video"
    OUTPUT_NODE = True
    CATEGORY = "image/video"

    def save_video(self, images, filename_prefix="video/ComfyUI", fps=24.0, format="mp4",
                   prompt=None, extra_pnginfo=None, **kwargs):
        if not HAS_AV:
            raise RuntimeError("PyAV (av) is not installed. Cannot save video.")

        full_output_folder, filename, counter, subfolder, filename_prefix = \
            folder_paths.get_save_image_path(filename_prefix, self.output_dir,
                                             images[0].shape[1], images[0].shape[0])

        custom_metadata = {}
        for i in range(20):
            name_key = f"meta_name_{i}"
            val_key = f"meta_value_{i}"
            if name_key in kwargs and val_key in kwargs:
                field_name = kwargs[name_key]
                if field_name and field_name.strip():
                    custom_metadata[field_name] = self._format_value(kwargs[val_key])

        file = f"{filename}_{counter:05}_.{format}"
        output_path = os.path.join(full_output_folder, file)

        open_options = {}
        if format == "mp4":
            open_options = {"movflags": "use_metadata_tags"}

        container = av.open(output_path, mode="w", options=open_options)

        if prompt is not None:
            container.metadata["prompt"] = json.dumps(prompt)
        if extra_pnginfo is not None:
            for key, value in extra_pnginfo.items():
                container.metadata[key] = json.dumps(value)

        if custom_metadata:
            container.metadata["custom_metadata"] = json.dumps(custom_metadata, indent=2)
            for key, value in custom_metadata.items():
                container.metadata[f"meta_{key}"] = str(value)

        codec_name = "libx264" if format == "mp4" else "libvpx-vp9"
        pix_fmt = "yuv420p"
        stream = container.add_stream(codec_name, rate=Fraction(round(fps * 1000), 1000))
        stream.width = images.shape[-2]
        stream.height = images.shape[-3]
        stream.pix_fmt = pix_fmt
        if format == "webm":
            stream.bit_rate = 0
            stream.options = {"crf": "32"}

        for frame_tensor in images:
            frame_np = torch.clamp(frame_tensor[..., :3] * 255, 0, 255).to(
                device=torch.device("cpu"), dtype=torch.uint8
            ).numpy()
            frame = av.VideoFrame.from_ndarray(frame_np, format="rgb24")
            for packet in stream.encode(frame):
                container.mux(packet)
        container.mux(stream.encode())
        container.close()

        results = [{"filename": file, "subfolder": subfolder, "type": self.type}]
        return {"ui": {"videos": results}}

    def _format_value(self, value):
        if isinstance(value, (int, float, str, bool)):
            return value
        elif isinstance(value, (list, tuple)):
            return list(value)
        elif hasattr(value, "item"):
            return value.item()
        else:
            return str(value)


# Node registration
NODE_CLASS_MAPPINGS = {
    "MetaSaver": MetaSaverNode,
    "MetaSaverDynamic": MetaSaverDynamicNode,
    "MetaVideoSaver": MetaVideoSaverNode,
    "MetaVideoSaverDynamic": MetaVideoSaverDynamicNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MetaSaver": "Save Image with Custom Metadata",
    "MetaSaverDynamic": "Save Image with Custom Metadata (Dynamic)",
    "MetaVideoSaver": "Save Video with Custom Metadata",
    "MetaVideoSaverDynamic": "Save Video with Custom Metadata (Dynamic)",
}
