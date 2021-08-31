from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version('retryable-requests')
except PackageNotFoundError:
    # package is not installed
    pass
