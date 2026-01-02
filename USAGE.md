# MetaSaver Usage Guide

This guide will walk you through using the MetaSaver node in ComfyUI.

## Quick Start

### 1. Installation

After installing the node (see [README.md](README.md)), restart ComfyUI. You should see two new nodes in the node menu:
- **Save Image with Custom Metadata** (MetaSaver)
- **Save Image with Custom Metadata (Dynamic)** (MetaSaverDynamic)

Both nodes work the same way - use whichever you prefer!

### 2. Basic Workflow

Here's a simple example to save an image with seed and prompt metadata:

**Step 1:** Add the MetaSaver node to your workflow
- Right-click → Add Node → image → Save Image with Custom Metadata

**Step 2:** Configure the number of metadata fields
- Set `num_metadata_fields` to `3` (for seed, positive prompt, negative prompt)

**Step 3:** Name your metadata fields
- `meta_name_0`: Enter `"seed"`
- `meta_name_1`: Enter `"positive_prompt"`
- `meta_name_2`: Enter `"negative_prompt"`

**Step 4:** Connect the values
- `meta_value_0`: Connect from your KSampler's `seed` output
- `meta_value_1`: Connect from your positive prompt text
- `meta_value_2`: Connect from your negative prompt text
- `images`: Connect from your VAE Decode or image source

**Step 5:** Run!
- Your image will be saved with all metadata embedded

## Common Patterns

### Pattern 1: Tracking Generation Parameters

Save all the important generation settings:

```
Number of fields: 5

Field 0: seed → (from KSampler seed)
Field 1: steps → (from KSampler steps)
Field 2: cfg_scale → (from KSampler cfg)
Field 3: sampler_name → (from KSampler sampler_name)
Field 4: scheduler → (from KSampler scheduler)
```

### Pattern 2: Model and LoRA Tracking

Keep track of what models you used:

```
Number of fields: 4

Field 0: base_model → (from checkpoint loader name)
Field 1: lora_1_name → (from LoRA loader 1 name)
Field 2: lora_1_strength → (from LoRA loader 1 strength)
Field 3: lora_2_name → (from LoRA loader 2 name)
```

### Pattern 3: Prompt Engineering

Save your prompts for later reference:

```
Number of fields: 3

Field 0: positive_prompt → (from CLIP text encode positive)
Field 1: negative_prompt → (from CLIP text encode negative)
Field 2: style_preset → (custom text input with style name)
```

### Pattern 4: Batch Processing

Track batch information:

```
Number of fields: 4

Field 0: batch_id → (custom text: "batch_001")
Field 1: variation_number → (from seed)
Field 2: timestamp → (custom text with date/time)
Field 3: notes → (custom text with notes)
```

## Advanced Usage

### Connecting Different Data Types

MetaSaver can handle various input types:

- **Integers**: Seeds, steps, etc.
- **Floats**: CFG scale, LoRA strengths, etc.
- **Strings**: Prompts, model names, notes
- **Arrays**: Can handle lists (they'll be converted to JSON arrays)

### Reading Metadata Later

**In ComfyUI:**
1. Drag your saved PNG back into the ComfyUI window
2. ComfyUI will load the workflow with all metadata

**In Python:**
```python
from PIL import Image
import json

img = Image.open("your_saved_image.png")

# Get structured metadata
custom_meta = json.loads(img.info["custom_metadata"])
print(f"Seed used: {custom_meta['seed']}")
print(f"Positive prompt: {custom_meta['positive_prompt']}")

# Or access individual fields
seed = img.info["meta_seed"]
```

**Using the example script:**
```bash
cd examples
python read_metadata.py ../output/your_image.png
```

**With ExifTool:**
```bash
exiftool your_image.png | grep -i meta
```

### Tips and Tricks

1. **Field Naming**: Use descriptive, consistent names
   - Good: `seed`, `positive_prompt`, `cfg_scale`
   - Avoid: `s`, `p`, `config`

2. **Optional Fields**: You don't have to fill all fields
   - Empty field names will be ignored
   - Useful for workflows where you sometimes need extra fields

3. **Workflow Organization**:
   - Group related metadata together
   - Number fields logically (0: seed, 1: steps, 2: cfg, etc.)

4. **Performance**:
   - Metadata adds minimal file size
   - No impact on generation speed

5. **Compatibility**:
   - Standard PNG format works everywhere
   - Metadata readable by any PNG-compatible tool
   - ComfyUI workflow data is preserved

## Troubleshooting

### "Node not found" error
- Make sure you've restarted ComfyUI after installation
- Check the console for any Python errors
- Verify the node folder is in `ComfyUI/custom_nodes/`

### Metadata not saving
- Ensure field names are not empty strings
- Check that values are properly connected
- Look at console for any error messages

### Can't read metadata
- Verify you're looking at the PNG file (not a preview)
- Try the included `read_metadata.py` script
- Check with `exiftool` to confirm metadata exists

### Values showing as strings
- This is normal - PNG text metadata stores everything as strings
- The `custom_metadata` field contains properly typed JSON
- Use `json.loads()` to parse it in Python

### Workflow not loading from saved image
- The ComfyUI workflow is separate from custom metadata
- Both are saved - workflow in `prompt` field, custom data in `custom_metadata`
- Dragging image into ComfyUI should restore the workflow

## Examples

See the `examples/` folder for:
- `read_metadata.py`: Script to read and export metadata
- More examples coming soon!

## Next Steps

- Try different metadata combinations
- Build a library of successful prompts with metadata
- Use metadata for A/B testing different parameters
- Share images with full generation context
- Create automated workflows using saved metadata

## Need Help?

- Check the [README.md](README.md) for more information
- Open an issue on GitHub
- Share your workflow for debugging

Happy generating! 🎨
