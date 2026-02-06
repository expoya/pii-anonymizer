// DOM Elements
const inputText = document.getElementById('inputText');
const outputText = document.getElementById('outputText');
const anonymizeBtn = document.getElementById('anonymizeBtn');
const copyBtn = document.getElementById('copyBtn');
const loading = document.getElementById('loading');
const errorMessage = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');
const inputCount = document.getElementById('inputCount');
const entityCount = document.getElementById('entityCount');
const entitiesInfo = document.getElementById('entitiesInfo');
const entitiesList = document.getElementById('entitiesList');
const languageRadios = document.querySelectorAll('input[name="language"]');

// State
let currentEntities = [];

// Event Listeners
anonymizeBtn.addEventListener('click', anonymizeText);
copyBtn.addEventListener('click', copyToClipboard);
inputText.addEventListener('input', updateInputCount);

// Initialize
updateInputCount();

// Get selected language
function getSelectedLanguage() {
    const selectedRadio = document.querySelector('input[name="language"]:checked');
    return selectedRadio ? selectedRadio.value : 'de';
}

// Update input character count
function updateInputCount() {
    const count = inputText.value.length;
    inputCount.textContent = `${count} Zeichen`;
}

// Anonymize text
async function anonymizeText() {
    const text = inputText.value.trim();

    if (!text) {
        showError('Bitte geben Sie einen Text ein.');
        return;
    }

    // Reset state
    hideError();
    outputText.value = '';
    copyBtn.disabled = true;
    currentEntities = [];
    entitiesInfo.style.display = 'none';

    // Show loading
    anonymizeBtn.disabled = true;
    loading.style.display = 'flex';

    try {
        const language = getSelectedLanguage();

        const response = await fetch('/anonymize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                language: language
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Fehler bei der Anonymisierung');
        }

        const data = await response.json();

        // Update output
        outputText.value = data.anonymized;
        currentEntities = data.entities;

        // Update entity count
        const count = data.entities.length;
        entityCount.textContent = count === 1
            ? '1 Entity erkannt'
            : `${count} Entities erkannt`;

        // Enable copy button if there's output
        if (data.anonymized) {
            copyBtn.disabled = false;
        }

        // Show entities info if any were found
        if (data.entities.length > 0) {
            displayEntities(data.entities);
        }

    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
    } finally {
        anonymizeBtn.disabled = false;
        loading.style.display = 'none';
    }
}

// Display detected entities
function displayEntities(entities) {
    if (entities.length === 0) {
        entitiesInfo.style.display = 'none';
        return;
    }

    entitiesList.innerHTML = '';

    entities.forEach(entity => {
        const item = document.createElement('div');
        item.className = 'entity-item';

        const type = document.createElement('span');
        type.className = 'entity-type';
        type.textContent = entity.type;

        const text = document.createElement('span');
        text.className = 'entity-text';
        text.textContent = entity.text;

        item.appendChild(type);
        item.appendChild(text);
        entitiesList.appendChild(item);
    });

    entitiesInfo.style.display = 'block';
}

// Copy to clipboard
async function copyToClipboard() {
    const text = outputText.value;

    if (!text) {
        return;
    }

    try {
        await navigator.clipboard.writeText(text);

        // Visual feedback
        const originalText = copyBtn.textContent;
        copyBtn.textContent = '✓ Kopiert!';
        copyBtn.style.backgroundColor = 'var(--success-color)';

        setTimeout(() => {
            copyBtn.textContent = originalText;
            copyBtn.style.backgroundColor = '';
        }, 2000);

    } catch (error) {
        console.error('Copy failed:', error);
        showError('Kopieren fehlgeschlagen. Bitte manuell kopieren.');
    }
}

// Show error message
function showError(message) {
    errorText.textContent = message;
    errorMessage.style.display = 'block';
}

// Hide error message
function hideError() {
    errorMessage.style.display = 'none';
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to anonymize
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        anonymizeText();
    }

    // Ctrl/Cmd + C when output is focused
    if ((e.ctrlKey || e.metaKey) && e.key === 'c' && document.activeElement === outputText) {
        copyToClipboard();
    }
});
