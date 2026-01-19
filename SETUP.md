# AI Coding Agent Evaluator - Configuration

This file contains helpful documentation for setting up and using the evaluator.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys

Create a `.env` file in the project root:

```bash
# Groq (optional - for fast cloud inference)
GROQ_API_KEY=gsk_...

# OpenAI (optional - for GPT-4)
OPENAI_API_KEY=sk-...
```

### 3. Set Up Ollama (Local Llama - optional)

```bash
# Install Ollama from https://ollama.ai
# Then pull the model
ollama pull llama2

# Ollama will automatically run on http://localhost:11434
```

### 4. Run the Application

#### Web UI (Recommended):
```bash
streamlit run app.py
```

#### Command Line:
```bash
python demo.py
```

## Model Configuration

### Groq (Fast Cloud LLM)
- **URL**: https://groq.com
- **Best for**: Fast, cost-effective evaluation
- **Models**: mixtral-8x7b-32768, llama2-70b, etc.
- **Setup**: Get API key from console.groq.com

### OpenAI (GPT-4)
- **URL**: https://openai.com
- **Best for**: Highest quality evaluation
- **Models**: gpt-4, gpt-3.5-turbo
- **Setup**: Get API key from platform.openai.com

### Ollama (Local Llama)
- **URL**: https://ollama.ai
- **Best for**: Privacy, offline evaluation, free
- **Models**: llama2, neural-chat, mistral
- **Setup**: Install Ollama, run `ollama pull llama2`

## Understanding the 15 Metrics

### Correctness & Functionality
1. **Task Success Rate**: % of tasks completed correctly (0-100%)
2. **Pass@1**: % chance first solution passes all tests (0-100%)

### Code Quality
3. **Multi-File Edit Accuracy**: % of correct multi-file changes (0-100%)
9. **Code Quality Score**: Readability, structure, maintainability (0-100)

### Planning & Problem Solving
4. **Planning Quality Score**: Quality of task decomposition (0-100)
5. **Tool Invocation Accuracy**: % of correct tool uses (0-100%)

### Memory & Context
6. **Context Retention**: % remembering prior steps/constraints (0-100%)
11. **Recovery Rate**: % self-correction without human help (0-100%)

### Safety & Security
7. **Hallucination Rate**: % inventing APIs/files (0-100%, lower is better)
8. **Scope Control**: % avoiding unnecessary changes (0-100%)
10. **Security Awareness**: % detecting insecure patterns (0-100%)

### Efficiency
12. **Latency per Step**: Seconds per reasoning step
13. **Token Efficiency**: Tokens consumed per successful task

### Consistency & Reliability
14. **Developer Intervention Rate**: % requiring human help (0-100%, lower is better)
15. **Output Stability**: % consistent results across runs (0-100%)

## Usage Examples

### Simple Evaluation
```python
from evaluator import AgentEvaluator, ModelType
from model_clients import GroqModelClient

# Setup
evaluator = AgentEvaluator()
groq_client = GroqModelClient()
evaluator.register_model(ModelType.GROQ, groq_client)

# Evaluate
result = evaluator.evaluate_task(
    task_id="my_task",
    problem_statement="Write a function to reverse a string",
    language="python",
    model_type=ModelType.GROQ
)

# Results
print(f"Score: {result.metrics.average()}/100")
print(f"Success: {result.metrics.task_success_rate}%")
```

### Compare Multiple Models
```python
from evaluator import AgentEvaluator, ModelType
from model_clients import (
    GroqModelClient,
    OpenAIModelClient,
    LlamaLocalClient
)

# Setup
evaluator = AgentEvaluator()
evaluator.register_model(ModelType.GROQ, GroqModelClient())
evaluator.register_model(ModelType.OPENAI, OpenAIModelClient())
evaluator.register_model(ModelType.LLAMA_LOCAL, LlamaLocalClient())

# Evaluate all models on same problem
problem = "Implement quicksort algorithm"

for model_type in [ModelType.GROQ, ModelType.OPENAI, ModelType.LLAMA_LOCAL]:
    result = evaluator.evaluate_task(
        task_id="sort_problem",
        problem_statement=problem,
        language="python",
        model_type=model_type
    )
    print(f"{result.model_name}: {result.metrics.average():.1f}/100")

# Export comparison
evaluator.export_results("comparison.json")
```

### Batch Evaluation
```python
tasks = [
    ("palindrome", "Find longest palindromic substring"),
    ("fibonacci", "Calculate fibonacci with memoization"),
    ("bfs", "Implement BFS traversal"),
]

for task_id, problem in tasks:
    result = evaluator.evaluate_task(
        task_id=task_id,
        problem_statement=problem,
        language="python",
        model_type=ModelType.GROQ,
        num_test_runs=3  # Run 3 times for stability
    )
    print(f"{task_id}: {result.metrics.average():.1f}/100")

summary = evaluator.get_summary_report()
```

## Running Tests

```bash
# Run all tests
pytest test_evaluator.py -v

# Run specific test
pytest test_evaluator.py::TestMetricsScore -v

# Run with coverage
pytest test_evaluator.py --cov=evaluator
```

## Troubleshooting

### "Model not registered" error
- Make sure API keys are set in `.env`
- Verify API keys are valid
- Check internet connection for cloud models

### Ollama connection error
- Verify Ollama is running: `ollama serve`
- Check connection to localhost:11434
- Pull model: `ollama pull llama2`

### JSON parsing errors
- Model response might not contain valid JSON
- Try with a shorter problem statement
- Use a different model

### Memory issues with local Llama
- Llama 2 needs ~4-8GB VRAM
- Use Ollama's quantized models if needed
- Or use cloud models instead

## Project Files

| File | Purpose |
|------|---------|
| `evaluator.py` | Core evaluation engine with 15 metrics |
| `model_clients.py` | Groq, OpenAI, Ollama client implementations |
| `app.py` | Streamlit web interface |
| `demo.py` | Example usage scripts |
| `test_evaluator.py` | Unit and integration tests |
| `requirements.txt` | Python dependencies |
| `README.md` | Project documentation |

## Extending the Framework

### Add a New Model
```python
class MyModelClient(ModelClient):
    def __init__(self):
        super().__init__(ModelType.GROQ, "my-model")
    
    def generate_test_cases(self, problem, language, num_cases=5):
        # Your implementation
        pass
    
    def evaluate_code(self, code, problem, language):
        # Your implementation
        pass
    
    def analyze_planning(self, problem):
        # Your implementation
        pass
```

### Add a New Metric
Edit `MetricsScore` dataclass in `evaluator.py` and update calculation logic.

### Add Test Cases
Add new test classes to `test_evaluator.py` following pytest conventions.

## Performance Notes

- **Groq**: ~0.5-2s per task (fastest)
- **OpenAI**: ~2-5s per task (highest quality)
- **Llama Local**: ~5-30s per task (varies by hardware)

Running evaluations with `num_test_runs=3` multiplies time by 3.

## Support

For issues or improvements:
1. Check existing code examples in `demo.py`
2. Review docstrings in `evaluator.py`
3. Look at unit tests in `test_evaluator.py`
