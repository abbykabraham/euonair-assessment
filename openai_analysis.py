import os
import json
import openai
from dotenv import load_dotenv

# Load environment
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found")

openai.api_key = openai_api_key

def analyze_abstract_openai(abstract: str) -> dict:
    """
    Uses OpenAI API (GPT-4) to extract the details from research papers abstract.
    It returns a JSON object with keys: "research_question", "objective", and "contribution".
    
    Parameters:
        abstract (str)
        
    Returns:
        dict: All extracted fields.
    """
    prompt = (
        "You are an experienced scientific paper reviewer. Given the abstract of a research paper, "
        "extract and output a valid JSON object with exactly the following keys: "
        "\"research_question\", \"objective\", and \"contribution\".\n\n"
        "Use these hints:\n"
        " - For research question: look for phrases such as 'How does', 'What is the impact of', etc.\n"
        " - For objective: look for phrases like 'The aim of this study is', 'Our objective is to', 'We aim to', etc.\n"
        " - For contribution: look for phrases like 'This study provides', 'The findings show', 'It contributes to', etc.\n\n"
        "For example, if the abstract is:\n"
        "\"Abstract: In this study, we investigate how X affects Y. Our objective is to develop a method to measure Z, "
        "and we demonstrate that A improves B compared to previous methods.\"\n\n"
        "Then the output should be:\n"
        "{\"research_question\": \"How does X affect Y?\", \"objective\": \"Develop a method to measure Z.\", "
        "\"contribution\": \"A improves B compared to previous methods.\"}\n\n"
        "Now, given the following abstract, output only a valid JSON object with no extra text.\n"
        "Abstract: " + abstract
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an experienced scientific paper reviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=256
        )
        message = response['choices'][0]['message']['content']
        print("Raw OpenAI response:", message)
        
        result = json.loads(message)
        result.setdefault("research_question", "Not identified")
        result.setdefault("objective", "Not identified")
        result.setdefault("contribution", "Not identified")
    except Exception as e:
        print("Error calling OpenAI API:", e)
        result = {
            "research_question": "Not identified",
            "objective": "Not identified",
            "contribution": "Not identified"
        }
    
    return result
