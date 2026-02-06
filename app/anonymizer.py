"""PII Anonymization using Microsoft Presidio."""

from typing import List, Dict
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from app.custom_recognizers import GermanTitleRecognizer


class PIIAnonymizer:
    """Handle PII detection and anonymization for German and English texts."""

    def __init__(self):
        """Initialize Presidio analyzer and anonymizer."""
        # Setup NLP engine for German and English
        configuration = {
            "nlp_engine_name": "spacy",
            "models": [
                {"lang_code": "de", "model_name": "de_core_news_lg"},
                {"lang_code": "en", "model_name": "en_core_web_lg"}
            ]
        }

        provider = NlpEngineProvider(nlp_configuration=configuration)
        nlp_engine = provider.create_engine()

        # Initialize analyzer with standard registry first
        self.analyzer = AnalyzerEngine(
            nlp_engine=nlp_engine,
            supported_languages=["de", "en"]
        )

        # Temporarily disable custom recognizer to test base functionality
        # german_title_recognizer = GermanTitleRecognizer()
        # self.analyzer.registry.add_recognizer(german_title_recognizer)

        # Initialize anonymizer
        self.anonymizer = AnonymizerEngine()

    def anonymize_text(self, text: str, language: str = "de") -> Dict:
        """
        Anonymize PII in the given text.

        Args:
            text: Input text containing PII
            language: Language code ("de" or "en")

        Returns:
            Dictionary with original text, anonymized text, and detected entities
        """
        if not text or not text.strip():
            return {
                "original": text,
                "anonymized": text,
                "entities": []
            }

        # Analyze text for PII entities
        analyzer_results = self.analyzer.analyze(
            text=text,
            language=language,
            entities=[
                "PERSON",
                "EMAIL_ADDRESS",
                "PHONE_NUMBER",
                "LOCATION",
                "DATE_TIME",
                "IBAN_CODE",
                "CREDIT_CARD",
                "IP_ADDRESS",
                "URL"
            ]
        )

        # Create anonymization config - replace with entity type in brackets
        # Define explicit operators for each entity type
        operators = {
            "PERSON": OperatorConfig("replace", {"new_value": "[PERSON]"}),
            "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "[EMAIL_ADDRESS]"}),
            "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "[PHONE_NUMBER]"}),
            "LOCATION": OperatorConfig("replace", {"new_value": "[LOCATION]"}),
            "DATE_TIME": OperatorConfig("replace", {"new_value": "[DATE_TIME]"}),
            "IBAN_CODE": OperatorConfig("replace", {"new_value": "[IBAN_CODE]"}),
            "CREDIT_CARD": OperatorConfig("replace", {"new_value": "[CREDIT_CARD]"}),
            "IP_ADDRESS": OperatorConfig("replace", {"new_value": "[IP_ADDRESS]"}),
            "URL": OperatorConfig("replace", {"new_value": "[URL]"}),
            "DEFAULT": OperatorConfig("replace", {"new_value": "[PII]"})
        }

        # Anonymize the text
        anonymized_result = self.anonymizer.anonymize(
            text=text,
            analyzer_results=analyzer_results,
            operators=operators
        )

        # Format detected entities for response
        entities = [
            {
                "type": result.entity_type,
                "text": text[result.start:result.end],
                "start": result.start,
                "end": result.end,
                "score": result.score
            }
            for result in analyzer_results
        ]

        return {
            "original": text,
            "anonymized": anonymized_result.text,
            "entities": entities
        }
