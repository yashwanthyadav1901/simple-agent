import os
import re
from openai import OpenAI
from dotenv import load_dotenv

# SETUP: Initialize the Nvidia Client
load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)

# --- 🛠️ IMPROVED TOOLS ---

def calculate(expression):
    try:
        # CLEANING: Remove commas and whitespace so eval() doesn't crash
        clean_expr = expression.replace(",", "").strip()
        return str(eval(clean_expr))
    except Exception as e:
        return f"Error: Could not calculate '{expression}'. Ensure you only use numbers and operators."

def search_web(query):
    # FLEXIBLE SEARCH: Check if keywords exist in our small database
    query = query.lower()
    database = {
        "tokyo": "37,000,000",
        "new york": "8,300,000",
        "paris": "2,100,000"
    }
    for key in database:
        if key in query:
            return database[key]
    return "Information not found. Try searching for just the city name."

tool_box = {
    "web_search": search_web,
    "calculator": calculate
}

# --- 🧠 IMPROVED PROMPT ---

SYSTEM_PROMPT = """
You are a Research Assistant. You follow this EXACT pattern:

Thought: [Reasoning]
Action: [tool_name]
Action Input: [input_data]

Then you MUST STOP and wait for an Observation. 
Available Tools: 'web_search' and 'calculator'.

Example:
Thought: I need the population of Tokyo.
Action: web_search
Action Input: Tokyo
Observation: 37,000,000
...and so on until:
Final Answer: [The result]
"""

def run_agent(question):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": question}]
    
    for i in range(10):
        print(f"\n--- 🧠 Step {i+1} ---")
        
        # We use a lower temperature to make the model less "creative" and more precise
        response = client.chat.completions.create(
            model="meta/llama-3.1-8b-instruct",
            messages=messages,
            temperature=0.1, 
            stop=["Observation:", "Observation"] # Force stop
        )
        
        content = response.choices[0].message.content.strip()
        print(content)

        if "Final Answer:" in content:
            return

        # Improved Parsing Logic
        try:
            action = re.search(r"Action:\s*(.*)", content).group(1).strip()
            action_input = re.search(r"Action Input:\s*(.*)", content).group(1).strip()
            
            if action in tool_box:
                result = tool_box[action](action_input)
                obs_text = f"Observation: {result}"
                print(f"🛠️ {obs_text}")
                
                # Append the agent's thought AND our observation to the history
                messages.append({"role": "assistant", "content": content})
                messages.append({"role": "user", "content": obs_text})
            else:
                messages.append({"role": "user", "content": f"Observation: Tool '{action}' not found."})
        except:
            messages.append({"role": "user", "content": "Observation: You forgot the Action/Action Input format. Please try again."})

run_agent("What is the population of Tokyo plus New York City?, give answer in millions")