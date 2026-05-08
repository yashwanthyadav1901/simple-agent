import os
import re
from openai import OpenAI
from dotenv import load_dotenv

# 1. SETUP: Initialize the Nvidia Client
load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)

# 2. THE TOOL: Our actual Python math function
def calculate(expression):
    try:
        # Note: eval() is used for simplicity here
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

# 3. THE SYSTEM PROMPT: The instructions for the 'Brain'
SYSTEM_PROMPT = """
You are an AI Agent that can use a calculator. 
You follow a strict loop: Thought, Action, Action Input, Observation.

If you need to do math, use the calculator tool.
Tool Name: calculator
Tool Input: A mathematical expression (e.g., "10 + 5 * 2")

Format your response exactly like this:
Thought: [Your reasoning about what to do]
Action: calculator
Action Input: [The math expression]

Wait for an Observation after you provide an Action.
When you have the final result, respond with:
Final Answer: [The final result]
"""

def run_agent(user_prompt):
    # This list acts as the agent's "Scratchpad" (Memory)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]
    
    # THE LOOP: Max 5 attempts to prevent infinite loops
    for i in range(5):
        print(f"\n--- 🔄 Step {i+1} ---")
        
        response = client.chat.completions.create(
            model="meta/llama-3.1-8b-instruct", # Or any Nvidia model you prefer
            messages=messages,
            stop=["Observation:"] # Tell the LLM to STOP after it asks for a tool
        )
        
        content = response.choices[0].message.content
        print(content)
        
        # Check if the agent is finished
        if "Final Answer:" in content:
            return content

        # PARSING: Look for Action and Action Input
        action_match = re.search(r"Action: (.+)", content)
        input_match = re.search(r"Action Input: (.+)", content)

        if action_match and input_match:
            tool_name = action_match.group(1).strip()
            tool_input = input_match.group(1).strip()

            if tool_name == "calculator":
                # EXECUTION: Run the Python code
                result = calculate(tool_input)
                observation = f"\nObservation: {result}"
                print(observation)
                
                # FEEDBACK: Add the Thought + Action + Observation back to memory
                messages.append({"role": "assistant", "content": content})
                messages.append({"role": "user", "content": observation})
            else:
                messages.append({"role": "user", "content": "Observation: Tool not found."})
        else:
            return "Error: Agent failed to follow the format."

# 4. RUN THE TEST
print(run_agent("What is 1234 multiplied by 56, and then add 789?"))