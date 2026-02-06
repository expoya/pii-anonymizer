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

    # Pattern for names with hyphens and multiple parts
    # Matches: Müller, Müller-Schmidt, Hans Müller, Hans-Peter Müller-Schmidt
    NAME_PATTERN = r"[A-ZÄÖÜ][a-zäöüß]+(?:-[A-ZÄÖÜ][a-zäöüß]+)*(?:\s+[A-ZÄÖÜ][a-zäöüß]+(?:-[A-ZÄÖÜ][a-zäöüß]+)*)?"

    PATTERNS = [
        Pattern(
            "herr_pattern",
            rf"\b(?:Herr|Herrn)\s+(?:Dr\.\s+|Prof\.\s+|Mag\.\s+|Dipl\.-Ing\.\s+)?({NAME_PATTERN})",
            0.85,
        ),
        Pattern(
            "frau_pattern",
            rf"\b(?:Frau)\s+(?:Dr\.\s+|Prof\.\s+|Mag\.\s+|Dipl\.-Ing\.\s+)?({NAME_PATTERN})",
            0.85,
        ),
        Pattern(
            "sehr_geehrte_pattern",
            rf"\bSehr\s+geehrte(?:r|s)?\s+(?:Herr|Herrn|Frau)\s+(?:Dr\.\s+|Prof\.\s+|Mag\.\s+)?({NAME_PATTERN})",
            0.9,
        ),
        Pattern(
            "liebe_pattern",
            rf"\b(?:Liebe|Lieber)\s+(?:Frau|Herr|Herrn)\s+({NAME_PATTERN})",
            0.85,
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
