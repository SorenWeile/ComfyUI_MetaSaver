"""
Example script to read metadata from images saved with MetaSaver node.

Usage:
    python read_metadata.py path/to/image.png
"""

import sys
import json
from PIL import Image


def read_metadata(image_path):
    """
    Read and display metadata from a PNG image saved by MetaSaver.

    Args:
        image_path: Path to the PNG image file
    """
    try:
        img = Image.open(image_path)

        print(f"\n{'='*60}")
        print(f"Metadata for: {image_path}")
        print(f"{'='*60}\n")

        # Check if image has metadata
        if not hasattr(img, 'info') or not img.info:
            print("No metadata found in this image.")
            return

        # Display custom metadata (structured JSON)
        if "custom_metadata" in img.info:
            print("📋 Custom Metadata (Structured):")
            print("-" * 60)
            try:
                custom_meta = json.loads(img.info["custom_metadata"])
                for key, value in custom_meta.items():
                    print(f"  {key}: {value}")
            except json.JSONDecodeError:
                print(f"  {img.info['custom_metadata']}")
            print()

        # Display individual metadata fields
        print("🏷️  Individual Metadata Fields:")
        print("-" * 60)
        meta_fields = {k: v for k, v in img.info.items()
                      if k.startswith("meta_")}
        if meta_fields:
            for key, value in meta_fields.items():
                display_key = key.replace("meta_", "")
                print(f"  {display_key}: {value}")
        else:
            print("  (No individual meta_ fields found)")
        print()

        # Display ComfyUI workflow metadata
        if "prompt" in img.info:
            print("⚙️  ComfyUI Workflow:")
            print("-" * 60)
            try:
                prompt_data = json.loads(img.info["prompt"])
                print(f"  Workflow contains {len(prompt_data)} nodes")
                # Display first few node types
                node_types = list(set(node.get("class_type", "Unknown")
                                    for node in prompt_data.values()))[:5]
                print(f"  Node types: {', '.join(node_types)}")
            except (json.JSONDecodeError, AttributeError):
                print("  (Unable to parse workflow)")
            print()

        # Display all other metadata keys
        other_meta = {k: v for k, v in img.info.items()
                     if k not in ["custom_metadata", "prompt", "workflow"]
                     and not k.startswith("meta_")}
        if other_meta:
            print("📎 Other Metadata:")
            print("-" * 60)
            for key, value in other_meta.items():
                # Truncate long values
                value_str = str(value)
                if len(value_str) > 100:
                    value_str = value_str[:100] + "..."
                print(f"  {key}: {value_str}")
            print()

        print(f"{'='*60}\n")

    except FileNotFoundError:
        print(f"Error: File not found: {image_path}")
    except Exception as e:
        print(f"Error reading metadata: {e}")


def export_metadata_json(image_path, output_path=None):
    """
    Export all metadata to a JSON file.

    Args:
        image_path: Path to the PNG image file
        output_path: Path for output JSON file (optional)
    """
    if output_path is None:
        output_path = image_path.rsplit(".", 1)[0] + "_metadata.json"

    try:
        img = Image.open(image_path)

        # Convert all metadata to JSON-serializable format
        metadata = {}
        for key, value in img.info.items():
            try:
                # Try to parse as JSON
                metadata[key] = json.loads(value)
            except (json.JSONDecodeError, TypeError):
                # Keep as string if not JSON
                metadata[key] = str(value)

        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        print(f"✅ Metadata exported to: {output_path}")

    except Exception as e:
        print(f"Error exporting metadata: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python read_metadata.py <image_path> [--export]")
        print("\nOptions:")
        print("  --export    Export metadata to JSON file")
        sys.exit(1)

    image_path = sys.argv[1]

    # Read and display metadata
    read_metadata(image_path)

    # Export to JSON if requested
    if "--export" in sys.argv:
        export_metadata_json(image_path)
