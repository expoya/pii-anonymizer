"""FastAPI application for PII anonymization."""

import logging
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from app.anonymizer import PIIAnonymizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="PII Anonymizer",
    description="Anonymize personally identifiable information from text",
    version="1.0.0"
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Initialize PII anonymizer (singleton)
try:
    anonymizer = PIIAnonymizer()
    logger.info("PIIAnonymizer initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize PIIAnonymizer: {e}")
    raise


class AnonymizeRequest(BaseModel):
    """Request model for anonymization."""
    text: str
    language: str = "de"


class AnonymizeResponse(BaseModel):
    """Response model for anonymization."""
    original: str
    anonymized: str
    entities: list


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve the main UI."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health_check():
    """Health check endpoint for Railway."""
    return {"status": "healthy", "service": "pii-anonymizer"}


@app.post("/anonymize", response_model=AnonymizeResponse)
async def anonymize(request: AnonymizeRequest):
    """
    Anonymize PII in the provided text.

    Args:
        request: AnonymizeRequest with text and language

    Returns:
        AnonymizeResponse with original, anonymized text and detected entities
    """
    try:
        # Validate language
        if request.language not in ["de", "en"]:
            raise HTTPException(
                status_code=400,
                detail="Language must be 'de' or 'en'"
            )

        # Validate text
        if not request.text or not request.text.strip():
            raise HTTPException(
                status_code=400,
                detail="Text cannot be empty"
            )

        logger.info(f"Anonymizing text (language: {request.language}, length: {len(request.text)})")

        # Anonymize the text
        result = anonymizer.anonymize_text(
            text=request.text,
            language=request.language
        )

        logger.info(f"Anonymization completed. Found {len(result['entities'])} entities")

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during anonymization: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
