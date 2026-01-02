# MetaSaver Quick Start Guide

## TL;DR

1. Add "Save Image with Custom Metadata" node
2. Fill in field names and connect values
3. Leave unused fields empty
4. Done!

## How It Works

The node shows you pairs of inputs like this:

```
meta_name_0: [text input]    meta_value_0: [any connection]
meta_name_1: [text input]    meta_value_1: [any connection]
meta_name_2: [text input]    meta_value_2: [any connection]
...
```

### To Add Metadata:

1. **Type a name** in `meta_name_X` (e.g., "seed", "prompt", "cfg_scale")
2. **Connect a value** to `meta_value_X` (from any node output)
3. Repeat for as many fields as you need
4. Leave the rest empty

### Example:

```
meta_name_0: "seed"              meta_value_0: ← connected from KSampler seed
meta_name_1: "positive_prompt"   meta_value_1: ← connected from CLIP Text Encode
meta_name_2: "cfg_scale"         meta_value_2: ← connected from KSampler cfg
meta_name_3: ""                  meta_value_3: [empty - ignored]
meta_name_4: ""                  meta_value_4: [empty - ignored]
```

## What Gets Saved?

Your metadata is embedded in the PNG file in two formats:

1. **Structured JSON** (in `custom_metadata` field):
   ```json
   {
     "seed": 12345,
     "positive_prompt": "beautiful landscape",
     "cfg_scale": 7.5
   }
   ```

2. **Individual fields** (as `meta_seed`, `meta_positive_prompt`, etc.)

## Reading Metadata

### Drag back into ComfyUI
Just drag the PNG into ComfyUI to restore the workflow!

### Python
```python
from PIL import Image
import json

img = Image.open("output.png")
metadata = json.loads(img.info["custom_metadata"])
print(metadata)
```

### Command Line
```bash
python examples/read_metadata.py output.png
```

## Tips

- **Empty = Ignored**: Fields with empty names are skipped
- **Any Type**: `meta_value_X` accepts ANY data type
- **Standard vs Dynamic**:
  - Standard = 10 field pairs
  - Dynamic = 20 field pairs
- **No Limit on Name Length**: Field names can be descriptive

## Common Patterns

### Pattern: Track Everything
```
meta_name_0: "seed"         → KSampler seed
meta_name_1: "steps"        → KSampler steps
meta_name_2: "cfg"          → KSampler cfg
meta_name_3: "sampler"      → KSampler sampler_name
meta_name_4: "scheduler"    → KSampler scheduler
meta_name_5: "model"        → CheckpointLoader name
```

### Pattern: Just Prompts
```
meta_name_0: "positive"     → Positive CLIP Text
meta_name_1: "negative"     → Negative CLIP Text
```

### Pattern: A/B Testing
```
meta_name_0: "test_id"      → Custom string "test_001"
meta_name_1: "variation"    → Custom string "red_background"
meta_name_2: "seed"         → KSampler seed
```

## Troubleshooting

**Q: I don't see all the fields!**
A: Scroll down in the node - they're all there (10 or 20 pairs depending on version)

**Q: My metadata isn't saving!**
A: Make sure the field name is filled in (not empty)

**Q: Can I use the same field name twice?**
A: Yes, but the last one will overwrite earlier ones. Use unique names.

**Q: What if I need more than 10/20 fields?**
A: Use two MetaSaver nodes, or open a GitHub issue to request more!

## Next Steps

- See [USAGE.md](USAGE.md) for detailed examples
- See [README.md](README.md) for full documentation
- Use `examples/read_metadata.py` to inspect saved metadata

Happy saving! 🎨
