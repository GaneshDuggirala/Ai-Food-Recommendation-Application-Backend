import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client with Groq base URL
api_key = os.environ.get("GROQ_API_KEY")
client = None
if api_key:
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

def extract_filters_with_ai(query: str, available_categories: list, available_tags: list) -> dict:

    if not client:
        print("GROQ_API_KEY is not set. Cannot use AI search.")
        return {}
        
    if not query.strip():
        return {}
        
    system_prompt = f"""You are a JSON query parser for a restaurant database.
Given a user's natural language request, extract the filtering parameters into a JSON object.


OUTPUT SCHEMA:
Return ONLY a valid JSON object with these exact keys. Use null/empty for fields not mentioned.
{{
  "keywords": ["list of strings", "extract variations/synonyms of the food terms, e.g., ['cake', 'cakes', 'sweet']"],
  "category": "string or null (try to closely match available categories if possible)",
  "dietary": ["list of strings", "or empty list (match available tags like Vegetarian, Non-Vegetarian, Gluten-Free)"],
  "is_fried": true, false, or null,
  "min_price": float or null (if the user mentions a minimum price or 'above X', e.g., 'above 10'),
  "max_price": float or null (if the user mentions a budget or max price, e.g., 'under 15')
}}

Do not include any markdown formatting, backticks, explanations, or other text. Just the JSON object.
"""

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            model="llama-3.3-70b-versatile", 
            temperature=0.0, 
        )
        
        response_text = chat_completion.choices[0].message.content.strip()
        
        if response_text.startswith("```"):
            lines = response_text.split('\n')
            if len(lines) >= 2:
                response_text = '\n'.join(lines[1:-1]).strip()
            
        filters = json.loads(response_text)
        print(json.dumps(filters, indent=2))
        
        return filters
    except Exception as e:
        print(f"AI Search Error: {e}")
        return {}
