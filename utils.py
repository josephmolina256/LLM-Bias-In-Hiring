from config import PROMPT_TEMPLATE, STRONG_RESUME_TEMPLATE, MEDIUM_RESUME_TEMPLATE, WEAK_RESUME_TEMPLATE
import json
from dotenv import load_dotenv




def resume_filler(resume_strength, first_name, last_name):
    """
    Generate a resume based on strength level and candidate names using templates.
    """
    if resume_strength == "strong":
        template = STRONG_RESUME_TEMPLATE
    elif resume_strength == "medium":
        template = MEDIUM_RESUME_TEMPLATE
    else:  # weak resume
        template = WEAK_RESUME_TEMPLATE
    
    return template.format(first_name=first_name, last_name=last_name)


def parse_response(response_text):
    """
    Parse the JSON response from the LLM.
    """
    try:
        data = json.loads(response_text)
        return {
            "decision": data["decision"],
            "score": int(data["score"]),
            "justification": data["justification"]
        }
    except Exception as e:
        print("Parse error:", e)
        return None

def build_prompt(name, resume, job_description):
    """
    Build the prompt for the LLM using the template.
    """
    return PROMPT_TEMPLATE.format(
        JOB_DESCRIPTION=job_description,
        RESUME=resume
    )

# Placeholder for OpenAI API call - replace with actual implementation
def call_openai(prompt):
    """
    Call Groq API with the prompt using OpenAI client.
    """
    from openai import OpenAI
    import os
    load_dotenv(override=True)  # Load environment variables from .env file
    
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")
    
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    
    return response.choices[0].message.content