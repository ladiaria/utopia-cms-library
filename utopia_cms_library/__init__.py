DIST_NAME = "utopia-cms-library"
DESCRIPTION = "A book management app for utopia-cms"


def get_version() -> str:
    """Version from installed distribution metadata (PEP 566)."""
    from importlib.metadata import version

    return version(DIST_NAME)


def __getattr__(name: str):
    if name == "__version__":
        v = get_version()
        globals()["__version__"] = v
        return v
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
