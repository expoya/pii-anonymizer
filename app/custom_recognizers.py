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

    # Simplified pattern for names - matches single or hyphenated surnames
    # More reliable than complex nested patterns
    PATTERNS = [
        Pattern(
            "german_title_name",
            r"\b(?:Sehr\s+geehrte(?:r|s)?\s+)?(?:Frau|Herr|Herrn)\s+(?:Dr\.|Prof\.|Mag\.|Dipl\.-Ing\.)?\s*([A-ZÄÖÜ][a-zäöüß]+(?:-[A-ZÄÖÜ][a-zäöüß]+)*(?:\s+[A-ZÄÖÜ][a-zäöüß]+(?:-[A-ZÄÖÜ][a-zäöüß]+)*)?)",
            0.75,
        ),
    ]

    CONTEXT = [
        "geehrte",
        "geehrter",
        "sehr",
        "liebe",
        "lieber",
        "von",
        "für",
    ]

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
