"""Custom exceptions for the RHOAI Reporter."""


class RHOAIReporterError(Exception):
    """Base exception for reporter errors."""
    pass


class VersionNotFoundError(RHOAIReporterError):
    """Requested RHOAI/OCP version combination not available."""
    pass


class DataParsingError(RHOAIReporterError):
    """Failed to parse catalog or markdown data."""
    pass


class GitHubAPIError(RHOAIReporterError):
    """GitHub API request failed."""
    pass