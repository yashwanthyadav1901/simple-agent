import json
import re
import os
from dotenv import load_dotenv
from openai import OpenAI

# SETUP
load_dotenv()

MODEL = "meta/llama-3.1-8b-instruct"
MAX_ITERATIONS = 5

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)

# THE TOOL
def get_weather(city):
    weather_map = {
        "tokyo": "Rainy",
        "new york": "Sunny",
        "london": "Cloudy"
    }
    return weather_map.get(city.lower(), "Sunny")

tool_box = {"get_weather": get_weather}

# THE SYSTEM PROMPT
SYSTEM_PROMPT = """
You are a Weather-Aware Travel Planner. Do not assume the weather of the destination.

You MUST follow this EXACT loop:

Step 1: Call the 'get_weather' tool using this format:
Thought: [Your reasoning]
Action: get_weather
Action Input: [city name]

IMPORTANT: After writing "Action Input:", STOP IMMEDIATELY.
Do NOT write the weather result yourself.
Do NOT write "[Weather API Response]", "Result:", or anything else.
locations should be real places in the city. not vague descriptions like "a park", "a museum". be specific.
Wait — the Observation will be provided to you.

Step 2: Once you receive the Observation, plan a 1-day itinerary:
    - If Rainy: Suggest indoor activities (museums, malls).
    - If Sunny: Suggest outdoor activities (parks, walking tours).
    - If Cloudy: Suggest a mix of both.

Step 3: Output ONLY this JSON as your final answer. No extra text.
{
  "city": "string",
  "weather": "string",
  "activity": "string",
  "location": "string"
}
"""

def extract_final_json(content):
    """
    Find all JSON blobs with a 'city' key and return the last one
    that also contains all required final-answer keys.
    """
    required_keys = {"city", "weather", "activity", "location"}
    candidates = re.findall(r"(\{[^{}]*\"city\"[^{}]*\})", content, re.DOTALL)

    for candidate in reversed(candidates):
        try:
            result = json.loads(candidate)
            if required_keys.issubset(result.keys()):
                return result
        except json.JSONDecodeError:
            continue

    return None


def run_weather_planner(city_query):
    print(f"\n🚀 Starting Weather Planner for: {city_query}")
    print("=" * 50)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Plan a trip for {city_query}"}
    ]

    seen_calls = set()

    for i in range(MAX_ITERATIONS):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.1,
            stop=["Observation:", "[Weather API Response]", "Result:", "Weather Result:"]
        )
        content = response.choices[0].message.content.strip()

        print(f"\n📍 Iteration {i + 1}:")
        print(f"Response:\n{content[:2000]}..." if len(content) > 2000 else f"Response:\n{content}")

        # 1. Try to extract the final answer JSON
        result = extract_final_json(content)
        if result:
            print("✅ Final JSON parsed successfully!")
            return result

        # 2. Try to parse and execute a tool call
        action_match = re.search(r"Action:\s*(.*)", content)
        input_match = re.search(r"Action Input:\s*(.*)", content)

        if action_match and input_match:
            action = action_match.group(1).strip()
            action_input = input_match.group(1).strip().strip('"\'')
            call_key = f"{action}:{action_input.lower()}"

            if call_key in seen_calls:
                print("⚠️ Repeated tool call detected — breaking to avoid infinite loop.")
                break

            if action in tool_box:
                seen_calls.add(call_key)
                tool_result = tool_box[action](action_input)
                obs_text = f"Observation: {tool_result}"

                messages.append({"role": "assistant", "content": content})
                messages.append({"role": "user", "content": obs_text})

                print(f"🛠️  Tool called : {action}({action_input})")
                print(f"🌦️  Weather result : {tool_result}")
            else:
                print(f"⚠️ Unknown tool '{action}' — breaking.")
                break
        else:
            print("⚠️ No tool call and no valid JSON found — model is stuck, breaking.")
            break

    print("❌ Agent exhausted all iterations without a valid result.")
    return None


# RUN THE SYSTEM
itinerary = run_weather_planner("london")
print("\n--- FINAL STRUCTURED ITINERARY ---")
if itinerary:
    print(json.dumps(itinerary, indent=2))
else:
    print("No itinerary could be generated.")