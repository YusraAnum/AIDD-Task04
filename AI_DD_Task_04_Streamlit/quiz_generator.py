
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate_quiz(text: str, num_questions: int = 5, quiz_type: str = "MCQ") -> str:
    """
    Generates quiz questions based on the provided text using the Gemini API.

    Args:
        text: The source text from which to generate quiz questions.
        num_questions: The desired number of questions.
        quiz_type: The type of quiz questions (e.g., "MCQ", "True/False", "Open-ended").

    Returns:
        A string containing the generated quiz questions.
        Returns an error message if the API key is not found or if the
        quiz generation fails.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY not found in environment variables."

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = (f"Generate {num_questions} {quiz_type} questions "
                  f"from the following text. Provide the answer for each question "
                  f"if it's MCQ or True/False. Make sure each question and its "
                  f"options/answer are clearly distinguishable. "
                  f"Text:\n\n{text}")
        
        response = model.generate_content(prompt)
        
        if response.parts:
            return response.text
        else:
            return "Error: Failed to generate quiz. The response was empty."

    except Exception as e:
        return f"An error occurred during quiz generation: {e}"

if __name__ == '__main__':
    # This is an example of how to use the function.
    # Make sure to set your GEMINI_API_KEY in a .env file in the same directory.
    
    sample_text = """
    The capital of France is Paris. The Eiffel Tower is located in Paris.
    The river Seine flows through Paris.
    """

    print("--- Generating MCQ Quiz ---")
    mcq_quiz = generate_quiz(sample_text, num_questions=2, quiz_type="MCQ")
    print(mcq_quiz)

    print("\n--- Generating True/False Quiz ---")
    tf_quiz = generate_quiz(sample_text, num_questions=2, quiz_type="True/False")
    print(tf_quiz)
