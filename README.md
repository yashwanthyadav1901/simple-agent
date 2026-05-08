# Simple AI Agent

An AI agent that performs mathematical calculations using an agentic loop pattern. The agent uses LLaMA 3.1 via the NVIDIA API to reason about math problems and execute calculations.

## Features

- **Agentic Loop**: Implements a Thought-Action-Observation loop for reasoning
- **Calculator Tool**: Execute mathematical expressions safely
- **Multi-step Reasoning**: Capable of breaking down complex math problems
- **Streaming Support**: Integrates with OpenAI-compatible APIs (NVIDIA, OpenAI, etc.)

## How It Works

The agent follows this pattern:
1. **Thought**: Reasons about the problem
2. **Action**: Decides to use the calculator tool
3. **Action Input**: Specifies the mathematical expression
4. **Observation**: Receives the calculation result
5. **Final Answer**: Provides the final result

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

Run the agent with a math problem:

```bash
python3 agent.py
```

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
