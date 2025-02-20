# Add no_default_download Option to SherpaOnnxClient

## Enhancement Request
Add an option to initialize SherpaOnnxClient without automatically downloading the default English model.

## Current Behavior
- SherpaOnnxClient downloads English model on initialization if no model/voice specified
- This is correct default behavior for standalone usage
- No way to prevent automatic download

## Proposed Change
Add `no_default_download` parameter to `__init__`:

```python
def __init__(
    self,
    model_path: str | None = None,
    tokens_path: str | None = None,
    model_id: str | None = None,
    no_default_download: bool = False,  # New parameter
) -> None:
```

## Use Cases
1. Voice management applications that need explicit control over downloads
2. Testing environments where automatic downloads are undesirable
3. Applications that want to defer model download until explicitly requested

## Impact
- Non-breaking change (default False maintains current behavior)
- Improves flexibility for application developers
- Helps with testing and development workflows
