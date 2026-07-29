import re
from typing import Optional

class PIISanitizer:
    """
    Sanitizes personal identifiable information (PII) from scraped job content
    to ensure compliance with DPDP Act 2023 guidelines (Section 3(c)(ii) data minimization).
    """

    # Email pattern matching standard and personal email addresses
    EMAIL_PATTERN = re.compile(
        r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        re.IGNORECASE
    )

    # Indian phone number pattern (matches +91, 0, or standard 10-digit mobile starting with 6-9)
    INDIAN_PHONE_PATTERN = re.compile(
        r'(?:\+?91[\-\s]?)?(?:0)?\b[6-9]\d{9}\b'
    )

    # General international phone pattern (e.g. +1 123 456 7890)
    GENERAL_PHONE_PATTERN = re.compile(
        r'\+?\d{1,3}[\s\-\.]?\(?\d{2,4}\)?[\s\-\.]?\d{3,4}[\s\-\.]?\d{3,4}'
    )

    REPLACEMENT_TEXT = "[Contact Via Application Link]"

    @classmethod
    def sanitize_text(cls, text: Optional[str]) -> str:
        """
        Strips personal emails and phone numbers from raw text.
        """
        if not text:
            return ""

        # Replace email addresses
        cleaned = cls.EMAIL_PATTERN.sub(cls.REPLACEMENT_TEXT, text)

        # Replace Indian phone numbers
        cleaned = cls.INDIAN_PHONE_PATTERN.sub(cls.REPLACEMENT_TEXT, cleaned)

        return cleaned

    @classmethod
    def sanitize_job_dict(cls, job_data: dict) -> dict:
        """
        Sanitizes all textual fields in a job dictionary.
        """
        sanitized = dict(job_data)
        for field in ("description", "job_description", "title", "raw_title"):
            if field in sanitized and isinstance(sanitized[field], str):
                sanitized[field] = cls.sanitize_text(sanitized[field])

        return sanitized
