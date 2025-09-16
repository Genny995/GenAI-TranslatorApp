# AI Translator
<br>

## Overview
This AI based application lets you pick a source language (with Automatic Detection avaiable), choose a target language, paste or type text, and get a single clean translaction. It includes a "Swap Languages" control (disabled when the source is *Automatic Detection*), basic validation, and a simple result area.
<br>

## Demo
Here's a quick demo of the translator in action:
<br>

![Translator Demo](assets/Translator_demo.gif)
<br>
<br>

## Model
- **Provider**: Groq (via langchain_groq)
- **Model**: *Gemma2-9b-It*
- **Rationale**: fast, quality general-purpose model suitable for short and medium-length translation tasks; served by Groq’s low-latency infrastructure.
<br>

## Tech Stack
- Python, Streamlit (UI)
- LangChain (prompt templating and chaining)
- langchain_groq (Groq LLM wrapper)
- python-dotenv (environment variables)
<br>

## How It Works (Architecture)
- Prompt templating with LangChain (*ChatPromptTemplate*) using variables: `origin_language`, `destination_language`, `text`.
- LLM wrapper: ChatGroq(model="*Gemma2-9b-It*") using `GROQ_API_KEY` from `.env`.
- Output parsing with *StrOutputParser* to return a plain string.
- A chain composes: prompt → model → parser.
- Streamlit UI provides language selectors, text input, Translate/Clear buttons, optional Swap Languages, and loading/error states.

### Core Prompt (exact)
- **System message**:
“*Translate the following text from {`origin_language`} to {`destination_language`} with just one version.*”
- **User message**:
“{`text`}”

### Features
- Source language select with “Automatic Detection”.
- Target language select (Automatic Detection is excluded as a target).
- “Swap Languages” to invert source/target (not allowed when source is Automatic Detection; an inline warning is shown).
- Text area for input and a dedicated output area for the translated text.
- Validation: checks for missing API key and empty input.
- Inline spinner and success/error messages.

### Supported Languages (current)
Automatic Detection (source only), Italian, English, Spanish, French, German, Chinese, Japanese, Dutch, Russian, Portuguese, Swedish.
**Note**: When using Automatic Detection, the app relies on the model’s implicit language detection (no explicit detection step is enforced by the prompt).

### Environment Variables
- `GROQ_API_KEY` — your Groq API key (required).
Optionally, you may set other variables for your development workflow, but they’re not required by the app.
<br>

## Local Setup & Run
1. (Optional) Create and activate a virtual environment.
2. Install dependencies (streamlit, python-dotenv, langchain, langchain-core, langchain-groq).
3. Create a .env file in the project root with GROQ_API_KEY=your_key.
4. Run the app with: streamlit run app.py
5. Open the local URL provided by Streamlit in your browser.
<br>

## Usage
1. Select the source language (or *Automatic Detection*) and the target language.
2. Enter or paste the text to translate.
3. Click *“Translate”* to get the translation.
4. Use *“Swap Languages”* to invert source/target (if source isn’t Automatic Detection).
5. Click *“Clear”* to reset the input area.
<br>

## Limitations & Notes
- Automatic Detection is implicit: the current system prompt does not instruct the model how to detect; it simply passes the text and the variables. Accuracy can vary for highly mixed-language inputs.
- Translations may vary for very long or domain-specific texts.
- The app does not persist any data; the input text is sent to Groq for processing.
- Network errors or invalid API keys will be surfaced via Streamlit error messages.
<br>
<br>

### Additional Material
For a step-by-step explaination and development notes, see the [Jupyter Notebook](notebooks/AI_translator.ipynb)
<br>

## Author
Gennaro Auricchio, 2025.