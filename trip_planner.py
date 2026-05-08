import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# SETUP: Initialize the Nvidia Client
load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)

# 1. THE STRUCTURED PROMPT
PLANNER_PROMPT = """
You are a Travel Planning Agent. 
Your goal is to create a structured itinerary.
You must respond ONLY with a valid JSON object. Do not include 'Thought' or 'Action' in your final response.

The JSON must follow this schema:
{
  "destination": "string",
  "duration_days": number,
  "daily_itinerary": [
    {"day": 1, "activity": "string", "location": "string"},
    ...
  ],
  "budget_estimate_usd": number
}
"""

def run_planner(user_input):
    print(f"📝 Planning for: {user_input}...")
    
    response = client.chat.completions.create(
        model="meta/llama-3.1-8b-instruct",
        messages=[
            {"role": "system", "content": PLANNER_PROMPT},
            {"role": "user", "content": user_input}
        ],
        response_format={ "type": "json_object" } # This is the magic line!
    )
    
    raw_json = response.choices[0].message.content
    
    # Convert string to Python Dictionary
    plan = json.loads(raw_json)
    return plan

# 2. RUN THE PLANNER
my_trip = run_planner("A 2-day food tour in New York City")

# Now we can access specific data points!
print(f"\n--- ✈️ Trip to {my_trip['destination']} ---")
for entry in my_trip['daily_itinerary']:
    print(f"Day {entry['day']}: {entry['activity']} at {entry['location']}")