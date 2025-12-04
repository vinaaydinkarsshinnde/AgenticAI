def is_cli_mode() -> bool:
    """Detect whether we are running in a CLI environment (True) or Streamlit (False)."""
    try:
        import streamlit.runtime as _rt  # type: ignore
        return not _rt.exists()
    except Exception:
        return True
