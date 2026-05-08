# Simple AI Agent Examples

A collection of AI agent implementations demonstrating agentic loops with reasoning and tool use. These examples use LLaMA 3.1 via the NVIDIA API to implement Thought-Action-Observation patterns.

## Featured Agents

### 1. Math Agent (`agent.py`)
An AI agent that performs mathematical calculations using an agentic loop pattern.
- **Tool**: Calculator for mathematical expressions
- **Pattern**: Thought → Action → Observation → Answer
- **Use Case**: Breaking down complex math problems and executing calculations

### 2. Weather-Aware Trip Planner (`trip_planner.py`)
An AI agent that plans day trips based on real-time weather conditions.
- **Tool**: Weather checker for destination cities
- **Pattern**: Check weather → Plan activities → Return structured itinerary
- **Use Case**: Context-aware travel planning with conditional logic

## Key Learnings

### JSON Extraction Challenges
When extracting JSON from LLM responses:
- **Problem**: Using `content.find("{"):content.rfind("}")` can capture multiple JSON objects or extra text, causing `JSONDecodeError: Extra data`
- **Solution**: Implement incremental parsing that tries to parse from the first `{` progressively until finding a valid JSON object
- **Better Solution**: Use regex to find specific JSON blobs with required keys (e.g., `required_keys.issubset(result.keys())`)

### System Prompt Design
- **Be explicit**: LLMs need clear instructions about WHEN to output JSON and what format to use
- **Use EXACT patterns**: Specify exact tool formats (Action/Action Input) to reduce parsing errors
- **Stop tokens matter**: Use `stop=["Observation:"]` to prevent the model from hallucinating results
- **Mock tools first**: Start with mock data to validate the loop before integrating real APIs

### Agent Loop Patterns
- **Iteration limits**: Always set `MAX_ITERATIONS` to prevent infinite loops
- **Robust parsing**: Use try-except when extracting structured data from LLM output
- **Tool validation**: Check if parsed action exists in `tool_box` before executing
- **Clear feedback**: Print debug info at each iteration to understand agent behavior

### Temperature & Determinism
- Use `temperature=0.1` for tool-using agents (reduces creativity, improves consistency)
- Use higher temperatures (0.7+) only when you want more varied reasoning

## Features

- **Agentic Loop**: Implements a Thought-Action-Observation loop for reasoning
- **Tool Execution**: Safely execute tools based on LLM decisions
- **Multi-step Reasoning**: Break down complex problems across iterations
- **Streaming Support**: Integrates with OpenAI-compatible APIs (NVIDIA, OpenAI, etc.)
- **Debug Output**: Clear iteration-by-iteration logging

## How Agents Work

### Basic Pattern
1. **Thought**: Reason about the problem
2. **Action**: Decide which tool to use
3. **Action Input**: Specify tool parameters
4. **Observation**: Receive tool result
5. **Final Answer**: Provide structured response

## Prerequisites

- Python 3.11+
- NVIDIA API key or OpenAI API key

## Installation

1. Clone or download this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set your API key as an environment variable:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

Or create a `.env` file in the project root:
```
OPENAI_API_KEY=your-api-key-here
```

## Usage

### Run the Math Agent
```bash
python3 agent.py
```

### Run the Trip Planner
```bash
python3 trip_planner.py
```

Both agents will print detailed iteration logs showing the reasoning process and tool calls.

The default example asks: "What is 1234 multiplied by 56, and then add 789?"

To modify the question, edit the last line in `agent.py`:
```python
print(run_agent("Your custom math question here"))
```

## Example Output

```
--- 🔄 Step 1 ---
Thought: I need to calculate 1234 multiplied by 56, then add 789. Let me use the calculator.
Action: calculator
Action Input: 1234 * 56 + 789

Observation: 70713

Final Answer: 1234 multiplied by 56 equals 69104, and then adding 789 equals 70713.
```

## Configuration

You can customize the agent by modifying:

- **Model**: Change `model="meta/llama-3.1-8b-instruct"` to use different models
- **API Base URL**: Modify `base_url` to point to different API endpoints
- **Max Iterations**: Adjust the `range(5)` loop to allow more/fewer reasoning steps
- **System Prompt**: Edit `SYSTEM_PROMPT` to change agent behavior

## Dependencies

- `openai` - OpenAI Python client for API calls
- `python-dotenv` - Load environment variables from `.env` file

## Limitations

- The agent has a maximum of 5 reasoning steps to prevent infinite loops
- Uses `eval()` for calculations (suitable for the controlled environment of this demo)
- Requires API credentials to run

## License

MIT
