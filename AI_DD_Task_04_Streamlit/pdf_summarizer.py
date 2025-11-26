
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def summarize_pdf_text(pdf_text: str) -> str:
    """
    Generates a summary of the given text using the Gemini API.

    Args:
        pdf_text: The text extracted from a PDF file.

    Returns:
        A string containing the summary of the text.
        Returns an error message if the API key is not found or if the
        summarization fails.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY not found in environment variables."

    try:
        genai.configure(api_key=api_key)
        model = model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"Please summarize the following text from a PDF:\n\n{pdf_text}"
        
        response = model.generate_content(prompt)
        
        if response.parts:
            return response.text
        else:
            # Handling cases where the response might be blocked or empty
            return "Error: Failed to generate summary. The response was empty."

    except Exception as e:
        return f"An error occurred during summarization: {e}"

if __name__ == '__main__':
    # This is an example of how to use the function.
    # Make sure to set your GEMINI_API_KEY in a .env file in the same directory.
    
    sample_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, 
    in contrast to the natural intelligence displayed by humans and other animals. 
    Leading AI textbooks define the field as the study of "intelligent agents": 
    any device that perceives its environment and takes actions that maximize its 
    chance of successfully achieving its goals.
    """

    print("--- Generating Summary ---")
    summary = summarize_pdf_text(sample_text)
    print(summary)

    # Example with a missing API key
    print("\n--- Testing Error Handling (Missing API Key) ---")
    original_key = os.environ.pop("GEMINI_API_KEY", None) # Temporarily remove key
    print(summarize_pdf_text(sample_text))
    if original_key:
        os.environ["GEMINI_API_KEY"] = original_key # Restore key
