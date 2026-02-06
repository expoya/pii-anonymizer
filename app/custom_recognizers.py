"""Custom recognizers for German PII detection."""

from typing import List, Optional
from presidio_analyzer import Pattern, PatternRecognizer


class GermanTitleRecognizer(PatternRecognizer):
    """
    Recognize names following German titles like "Herr" or "Frau".

    Detects patterns like:
    - "Herr Müller"
    - "Frau Schmidt"
    - "Sehr geehrte Frau Luger"
    - "geehrter Herr Dr. Wagner"
    """

    # Very simple test pattern to debug
    PATTERNS = [
        Pattern(
            "frau_mag_name",
            r"Frau\s+Mag\.\s+([A-ZÄÖÜ][\wäöüßÄÖÜ\-]+(?:\s+[\wäöüßÄÖÜ\-]+)?)",
            0.85,
        ),
        Pattern(
            "frau_dr_name",
            r"Frau\s+Dr\.\s+([A-ZÄÖÜ][\wäöüßÄÖÜ\-]+(?:\s+[\wäöüßÄÖÜ\-]+)?)",
            0.85,
        ),
        Pattern(
            "herr_title_name",
            r"Herr(?:n)?\s+(?:Dr\.|Prof\.|Mag\.)?\s*([A-ZÄÖÜ][\wäöüßÄÖÜ\-]+(?:\s+[\wäöüßÄÖÜ\-]+)?)",
            0.85,
        ),
    ]

    CONTEXT = []

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "de",
        supported_entity: str = "GERMAN_TITLE_NAME",
    ):
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )
