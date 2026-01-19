# AI Coding Agent Evaluator

A comprehensive evaluation framework for testing and comparing AI coding assistants (both local and cloud models) across **15 core metrics**.

## 🚀 Features

- **Multi-Model Support**: Evaluate Groq, OpenAI GPT-4, and Local Llama 2 (via Ollama)
- **15 Core Metrics**: Comprehensive evaluation across correctness, efficiency, code quality, security, and more
- **Automated Test Case Generation**: Generate test cases from problem statements
- **Detailed Reporting**: Export results as JSON or CSV
- **Web UI**: Streamlit interface for easy comparison and visualization
- **Batch Evaluation**: Test multiple models on same tasks
- **Stability Measurement**: Run multiple iterations to measure consistency

## 📊 15 Core Metrics

| # | Metric | Description |
|---|--------|-------------|
| 1️⃣ | **Task Success Rate** | Percentage of tasks completed correctly end-to-end |
| 2️⃣ | **Pass@1** | Probability the first solution passes all tests |
| 3️⃣ | **Multi-File Edit Accuracy** | Correctness of changes across multiple files |
| 4️⃣ | **Planning Quality Score** | How well the agent decomposes tasks |
| 5️⃣ | **Tool Invocation Accuracy** | Correct usage of tools (file edits, commands, etc.) |
| 6️⃣ | **Context Retention** | Memory of prior steps, files, and constraints |
| 7️⃣ | **Hallucination Rate** | Frequency of invented APIs, files, or behaviors |
| 8️⃣ | **Scope Control** | Avoids unnecessary or risky changes |
| 9️⃣ | **Code Quality Score** | Readability, structure, maintainability |
| 🔟 | **Security Awareness** | Detection and avoidance of insecure patterns |
| 1️⃣1️⃣ | **Recovery Rate** | Ability to detect and fix mistakes |
| 1️⃣2️⃣ | **Latency per Step** | Time taken per reasoning or execution step |
| 1️⃣3️⃣ | **Token Efficiency** | Tokens consumed per successful task |
| 1️⃣4️⃣ | **Developer Intervention Rate** | How often a human must step in |
| 1️⃣5️⃣ | **Output Stability** | Consistency of results across runs |

## 🛠️ Tech Stack

- **LangChain**: Multi-model LLM orchestration
- **Groq**: Fast cloud LLM API
- **OpenAI**: GPT-4 for evaluation
- **Ollama**: Local Llama 2 execution
- **Streamlit**: Web UI
- **Pandas & Plotly**: Data visualization

## ⚙️ Installation

### Prerequisites
- Python 3.10+
- For local Llama: [Ollama](https://ollama.ai) running on localhost:11434

### Setup

```bash
# Clone and navigate
cd /home/tw10577/eval

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cat > .env << EOF
GROQ_API_KEY=your_groq_key_here
OPENAI_API_KEY=your_openai_key_here
EOF
```

## 🚀 Usage

### Option 1: Web UI (Recommended)

```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

**Features:**
- Interactive model selection
- Predefined coding tasks or custom problems
- Real-time evaluation progress
- Detailed metrics comparison
- Export results as JSON/CSV

### Option 2: Python Script

```bash
python demo.py
```

Or use the evaluator in your code:

```python
from evaluator import AgentEvaluator, ModelType
from model_clients import GroqModelClient

# Initialize
evaluator = AgentEvaluator()
groq_client = GroqModelClient()
evaluator.register_model(ModelType.GROQ, groq_client)

# Evaluate a task
result = evaluator.evaluate_task(
    task_id="task_001",
    problem_statement="Write a function to reverse a string",
    language="python",
    model_type=ModelType.GROQ,
    num_test_runs=3
)

# View results
print(f"Overall Score: {result.metrics.average()}/100")
print(f"Task Success: {result.metrics.task_success_rate}%")

# Export
evaluator.export_results("results.json")
```

## 📁 Project Structure

```
eval/
├── evaluator.py          # Core evaluation engine + 15 metrics
├── model_clients.py      # Groq, OpenAI, Llama clients
├── app.py               # Streamlit web interface
├── demo.py              # Example usage
├── requirements.txt     # Dependencies
├── .env                 # API keys (create this)
└── README.md            # This file
```

## 🔑 API Keys

You need to set up the following (optional - use only models you need):

### Groq
1. Get API key from [console.groq.com](https://console.groq.com)
2. Add to `.env`: `GROQ_API_KEY=your_key`

### OpenAI
1. Get API key from [platform.openai.com](https://platform.openai.com)
2. Add to `.env`: `OPENAI_API_KEY=your_key`

### Local Llama (Free)
1. Install [Ollama](https://ollama.ai)
2. Run: `ollama pull llama2`
3. Ollama will serve on `http://localhost:11434` automatically

## 📊 Example Output

```
Model Comparison:
==================================================

Groq (mixtral-8x7b-32768):
  Overall Score: 87.5/100
  Task Success Rate: 92.0%
  Code Quality: 85.0/100
  Context Retention: 88.0%
  Hallucination Rate: 3.0%

OpenAI (gpt-4):
  Overall Score: 91.2/100
  Task Success Rate: 95.0%
  Code Quality: 89.0/100
  Context Retention: 92.0%
  Hallucination Rate: 2.0%

Llama 2 (Local):
  Overall Score: 76.8/100
  Task Success Rate: 80.0%
  Code Quality: 75.0/100
  Context Retention: 78.0%
  Hallucination Rate: 8.0%
```

## 🔍 How It Works

### Evaluation Flow

1. **Input**: Problem statement + programming language
2. **Test Case Generation**: AI generates 5+ test cases
3. **Planning Analysis**: Evaluates task decomposition quality
4. **Code Quality Assessment**: Rates readability, maintainability, efficiency
5. **Multi-Run Testing**: Runs evaluation N times to measure stability
6. **Aggregation**: Combines results into 15 core metrics
7. **Comparison**: Visualizes model performance differences

### Metrics Calculation

- **Correctness Metrics** (Pass@1, Task Success): Based on test case passage
- **Quality Metrics** (Code Quality, Planning): AI-evaluated on 0-100 scale
- **Safety Metrics** (Hallucination, Scope Control): Detection of problematic patterns
- **Performance Metrics** (Latency, Token Efficiency): Measured per step
- **Stability**: Standard deviation across multiple runs

## 📈 Roadmap

- [ ] Support for more cloud providers (Anthropic, Hugging Face)
- [ ] Real-time metrics dashboard
- [ ] Benchmark dataset with 100+ problems
- [ ] Integration with GitHub for CI/CD evaluation
- [ ] Cost analysis per model
- [ ] Custom metric definitions
- [ ] Regression testing framework

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- Add more model providers
- Enhance metric calculations
- Improve test case generation
- Add visualization dashboards
- Performance optimizations

## 📄 License

MIT License - Feel free to use in your projects

## 📞 Support

For issues or questions:
1. Check the demo.py for usage examples
2. Review evaluator.py for metric definitions
3. See model_clients.py for LLM integration patterns

---

**Last Updated**: January 2026
**Version**: 1.0.0
