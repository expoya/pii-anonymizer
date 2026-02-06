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

    PATTERNS = [
        Pattern(
            "herr_pattern",
            r"\b(?:Herr|Herrn)\s+(?:Dr\.\s+|Prof\.\s+|Mag\.\s+|Dipl\.-Ing\.\s+)?([A-ZÄÖÜ][a-zäöüß]+(?:\s+[A-ZÄÖÜ][a-zäöüß]+)?)",
            0.85,
        ),
        Pattern(
            "frau_pattern",
            r"\b(?:Frau)\s+(?:Dr\.\s+|Prof\.\s+|Mag\.\s+|Dipl\.-Ing\.\s+)?([A-ZÄÖÜ][a-zäöüß]+(?:\s+[A-ZÄÖÜ][a-zäöüß]+)?)",
            0.85,
        ),
        Pattern(
            "sehr_geehrte_pattern",
            r"\bSehr\s+geehrte(?:r|s)?\s+(?:Herr|Herrn|Frau)\s+(?:Dr\.\s+|Prof\.\s+|Mag\.\s+)?([A-ZÄÖÜ][a-zäöüß]+(?:\s+[A-ZÄÖÜ][a-zäöüß]+)?)",
            0.9,
        ),
        Pattern(
            "liebe_pattern",
            r"\b(?:Liebe|Lieber)\s+(?:Frau|Herr|Herrn)\s+([A-ZÄÖÜ][a-zäöüß]+)",
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
        supported_entity: str = "PERSON",
    ):
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )
