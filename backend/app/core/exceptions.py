class FMPAPIError(Exception):
    """Custom exception for errors returned by the FMP API."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class RateLimitError(FMPAPIError):
    """Custom exception for when the FMP API rate limit is hit."""
    def __init__(self, message: str = "FMP API rate limit exceeded."):
        self.message = message
        super().__init__(self.message)

class DataValidationError(Exception):
    """Custom exception for Pydantic data validation errors."""
    def __init__(self, model: str, errors: any):
        self.model = model
        self.errors = errors
        message = f"Data validation failed for {model}: {errors}"
        super().__init__(message)