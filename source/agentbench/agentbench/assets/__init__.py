from pathlib import Path 

# Resolve debug assets directory: works in both source and installed environments
def _find_debug_assets_dir():
    """Resolve bundled debug assets relative to this source or installed package."""
    current = Path(__file__).resolve()
    for parent in [current.parent] + list(current.parents):
        debug_assets_path = parent / "assets" / "debug_assets"
        if debug_assets_path.exists() and debug_assets_path.is_dir():
            # Verify a test file exists
            test_file = debug_assets_path / "013_apple/013_apple.usd"
            if test_file.exists():
                return debug_assets_path
    
    # Fallback to relative path (may not exist, but preserves original behavior)
    return Path(__file__).parent.resolve() / "assets" / "debug_assets"

DEBUG_YCB_OBJ_DIR = str(_find_debug_assets_dir())
