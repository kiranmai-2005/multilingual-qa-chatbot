import requests
import json
import os # Import os for environment variables
from .wikipedia_fetcher import get_context_from_wikipedia # Keep for RAG
from .translate import translate_text # Import translate_text for internal use

# API key for Gemini. It will be read from the GOOGLE_API_KEY environment variable.
# Ensure you set this environment variable before running the Streamlit app.
API_KEY = os.getenv("GOOGLE_API_KEY", "")
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def answer_question(question, src_lang):
    """
    Answers a question by:
    1. Translating the question to English (if needed).
    2. Fetching context from Wikipedia based on the English question.
    3. Using a Google LLM (Gemini API) to answer the question,
       augmented with Wikipedia context.
    4. Returns the answer.
    """
    try:
        if not API_KEY:
            # More explicit error message if API_KEY is not set
            raise ValueError("API_KEY is not set. Please set the GOOGLE_API_KEY environment variable in your terminal before running the app. Refer to README.md for instructions.")

        # Translate the incoming question to English for Wikipedia search
        # Wikipedia search often works best with English queries.
        question_en = translate_text(question, src_lang, "en")
        print(f"Translated question to English for QA: {question_en}") # Debugging

        # Get context from Wikipedia using the English question
        context = get_context_from_wikipedia(question_en)

        # --- DEBUGGING PRINTS (CRUCIAL FOR DIAGNOSIS) ---
        print(f"\n--- DEBUG: Context for LLM (from Wikipedia) ---\n")
        print(context)
        print(f"\n--- DEBUG END ---\n")
        # -------------------------------------------------

        # Construct the prompt for the LLM
        prompt = ""
        # Check if the original question asks for current information or a specific person
        is_who_is_query = any(keyword in question.lower() for keyword in ["who is", "who's", "name of"])

        # Modified instruction to explicitly force the name first for "who is" questions
        if is_who_is_query:
            # This instruction is designed to strongly guide the LLM to output the name first,
            # then the role. It tries to enforce a specific sentence structure.
            prompt = (
                f"For the question '{question}', state the full name of the person being asked about first. "
                f"Your answer MUST start with 'The [role] of [country] is [Full Name].' (e.g., 'The Prime Minister of India is Narendra Modi.') "
                f"followed by other relevant concise details if available. "
                f"Use the provided context if relevant, otherwise use your general knowledge. "
                f"Do NOT mention that you lack current information, internet access, or that the answer is not in the context. "
                f"Answer in the original language of the question ('{question}') if possible, otherwise in English.\n\n"
                f"Question: '{question}'\n\n"
            )
        else:
            # General instruction for other types of questions
            prompt = (
                f"Answer the following question concisely and accurately. "
                f"Use the provided context if relevant, otherwise answer based on your general knowledge. "
                f"Do NOT mention that you lack current information, internet access, or that the answer is not in the context. "
                f"Answer in the original language of the question ('{question}') if possible, otherwise in English:\n\n"
                f"Question: '{question}'\n\n"
            )

        # Append context only if it's substantial and relevant
        if context and context.strip() != "Sorry, no relevant context could be retrieved from Wikipedia." and len(context.strip()) >= 50:
            prompt += f"Context: '{context}'"
        else:
            print("No sufficient context found from Wikipedia or context too short. Relying on general knowledge.")

        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}]
        }
        headers = {'Content-Type': 'application/json'}
        params = {'key': API_KEY}

        # --- DEBUGGING PRINTS (CRUCIAL FOR DIAGNOSIS) ---
        print(f"\n--- DEBUG: Prompt sent to LLM ---\n")
        print(prompt)
        print(f"\n--- DEBUG END ---\n")
        # -------------------------------------------------

        response = requests.post(API_URL, headers=headers, params=params, data=json.dumps(payload))
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        result = response.json()

        if result.get("candidates") and result["candidates"][0].get("content") and result["candidates"][0]["content"].get("parts"):
            answer = result["candidates"][0]["content"]["parts"][0]["text"].strip()
            print(f"LLM Answer: '{answer}'")
            return answer
        
        print(f"LLM did not return a valid answer. API response: {result}")
        return "Sorry, I could not generate an answer."

    except requests.exceptions.RequestException as e:
        print(f"API request error during question answering: {e}")
        return f"An API error occurred while answering the question: {e}"
    except Exception as e:
        print(f"An unexpected error occurred in answer_question: {e}")
        return f"An error occurred while answering the question: {e}"

