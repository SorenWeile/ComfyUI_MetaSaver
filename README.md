# ComfyUI MetaSaver

A powerful ComfyUI custom node for saving images **and videos** with flexible custom metadata fields embedded directly in the file.

## Features

- **Up to 10 Metadata Fields**: Standard version with 10 optional metadata slots
- **Up to 20 Metadata Fields**: Dynamic version with 20 optional metadata slots
- **Custom Field Names**: Give each metadata field a custom name
- **Flexible Input Types**: Supports ANY type - strings, integers (seeds), floats (CFG), and more
- **PNG & Video Metadata Embedding**: Custom data saved in PNG files or video container tags
- **Workflow Preservation**: Maintains standard ComfyUI workflow metadata
- **Multiple Formats**: Metadata saved both as structured JSON and individual fields
- **All Optional**: Only fill in the fields you need - empty fields are ignored
- **Video Output**: Save MP4 (H.264) or WEBM (VP9) video from image frame batches

## Why MetaSaver?

Unlike standard save nodes, MetaSaver lets you:
- Save **seeds** from KSampler nodes
- Store **positive and negative prompts**
- Record **model names, LoRA weights, CFG values**
- Add **any custom text or numbers** you want to track
- **Name your fields** exactly how you want them
- **Embed metadata in videos** as container-level tags

Perfect for tracking generation parameters, comparing outputs, or sharing images and videos with full context!

## Installation

### Method 1: ComfyUI Manager (Recommended)
1. Open ComfyUI Manager
2. Search for "MetaSaver"
3. Click Install

### Method 2: Manual Installation
1. Navigate to your ComfyUI custom_nodes directory:
   ```bash
   cd ComfyUI/custom_nodes/
   ```

2. Clone this repository:
   ```bash
   git clone https://github.com/SorenWeile/ComfyUI_MetaSaver.git
   ```

3. Restart ComfyUI

## Usage

### Saving Images

1. Add the **"Save Image with Custom Metadata"** node to your workflow
2. You'll see pairs of inputs for metadata (10 pairs in standard, 20 in dynamic version):
   - `meta_name_0`: Name of first field (e.g., "seed")
   - `meta_value_0`: Value to save (e.g., connect from KSampler seed output)
   - `meta_name_1`: Name of second field (e.g., "positive_prompt")
   - `meta_value_1`: Value to save
   - ... and so on

3. Fill in only the metadata fields you want to use (empty ones are ignored)
4. Connect your image output to the `images` input
5. Run your workflow!

### Saving Videos

1. Add the **"Save Video with Custom Metadata"** node to your workflow
2. Connect an `IMAGE` batch (your video frames) to the `images` input
3. Set `fps`, choose `format` (mp4 or webm), and fill in any metadata fields
4. Run your workflow — the video is saved to your ComfyUI output folder

A typical video workflow: **KSampler → VAE Decode → Save Video with Custom Metadata**

Or for multi-frame video: connect the image batch output from a video model directly.

**Note**: All metadata fields are optional - you can use as many or as few as you need!

### Reading Metadata

**From PNG images:**
- ComfyUI: Drag the image back into ComfyUI to see all metadata
- Python:
  ```python
  from PIL import Image
  img = Image.open("your_image.png")
  metadata = img.info.get("custom_metadata")
  print(metadata)
  ```
- ExifTool: `exiftool your_image.png`

**From MP4/WEBM videos:**
- Command line: `ffprobe -v quiet -print_format json -show_format your_video.mp4`
- Python:
  ```python
  import av, json
  with av.open("your_video.mp4") as container:
      custom = json.loads(container.metadata.get("custom_metadata", "{}"))
      print(custom)
  ```
- ExifTool: `exiftool your_video.mp4`

The metadata JSON structure is the same for both images and videos:
```json
{
  "seed": 12345,
  "positive_prompt": "a beautiful landscape",
  "cfg_scale": 7.5,
  "model_name": "sd_xl_base_1.0"
}
```

## Node Variants

### MetaSaver (Standard)
Saves a **PNG image** with **10 optional metadata field pairs** (meta_name_0 through meta_name_9).
Perfect for most use cases.

### MetaSaverDynamic (Advanced)
Saves a **PNG image** with **20 optional metadata field pairs** (meta_name_0 through meta_name_19).
For power users who need to track many parameters at once.

### MetaVideoSaver (Standard)
Saves a **video (MP4 or WEBM)** from an `IMAGE` batch with **10 optional metadata field pairs**.
Metadata is embedded as container-level tags readable by ffprobe, ExifTool, or PyAV.

### MetaVideoSaverDynamic (Advanced)
Saves a **video (MP4 or WEBM)** from an `IMAGE` batch with **20 optional metadata field pairs**.

## Common Use Cases

1. **Track Generation Parameters**:
   - Seed, steps, CFG scale, sampler name
   - Easy to reproduce exact results later

2. **Model Comparison**:
   - Save model name, version, hash
   - Compare outputs from different models

3. **Prompt Engineering**:
   - Store positive/negative prompts with images
   - Build a library of what works

4. **LoRA Experimentation**:
   - Record LoRA names and weights
   - Track which combinations work best

5. **Batch Processing**:
   - Add batch IDs, timestamps, custom notes
   - Organize large generation runs

## Technical Details

- **Image Format**: PNG with embedded metadata (PIL/Pillow)
- **Video Formats**: MP4 (H.264, yuv420p) or WEBM (VP9, yuv420p) via PyAV
- **Metadata Storage**: Structured JSON + individual text fields (images); container-level tags (videos)
- **MP4 Metadata**: Written using `movflags=use_metadata_tags` for full tag support
- **ComfyUI Integration**: Follows standard node conventions
- **Workflow Compatibility**: Preserves standard ComfyUI workflow data (prompt + extra_pnginfo)


## Troubleshooting

### Node doesn't appear in ComfyUI
- Restart ComfyUI completely
- Check that the folder is in `ComfyUI/custom_nodes/`
- Look for errors in the console

### Metadata not saving
- Ensure field names are not empty
- Check that values are connected to inputs
- For images: verify PNG format is selected
- For videos: use `ffprobe -show_format_tags` to inspect saved file

### Can't read metadata
- Images: use `exiftool` or Python PIL — check the `custom_metadata` field for structured JSON
- Videos: use `ffprobe -v quiet -print_format json -show_format your_video.mp4`
- Individual fields are prefixed with `meta_` in the Dynamic variant

### Video node not available
- Ensure PyAV is installed: `pip install av`
- PyAV is bundled with most ComfyUI distributions — check the console for import errors

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - see LICENSE file for details

## Credits

Inspired by excellent existing nodes:
- [ComfyUI-SaveImageWithMetaData](https://github.com/nkchocoai/ComfyUI-SaveImageWithMetaData)
- [comfy-image-saver](https://github.com/giriss/comfy-image-saver)
- [ComfyUI-Crystools](https://github.com/crystian/ComfyUI-Crystools)

## Support

Found a bug or have a feature request?
- Open an issue on GitHub
- Provide workflow examples if possible
- Include ComfyUI console errors

---

**Enjoy tracking your AI generations with full metadata control!** 🎨✨
