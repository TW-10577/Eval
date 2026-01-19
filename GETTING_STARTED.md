# AI Coding Agent Evaluator - Complete Setup Guide

## 📦 Project Created Successfully!

You now have a comprehensive evaluation framework for testing AI coding assistants across **15 core metrics** using both local and cloud LLM models.

## 📂 Files Created

```
/home/tw10577/eval/
├── evaluator.py                 # Core evaluation engine (main logic)
├── model_clients.py             # LLM client implementations
├── app.py                       # Streamlit web interface
├── demo.py                      # Example usage & demos
├── test_evaluator.py            # Unit tests
├── requirements.txt             # Dependencies
├── README.md                    # Full documentation
├── SETUP.md                     # Setup & configuration guide
└── .env.example                 # Environment template
```

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
cd /home/tw10577/eval
pip install -r requirements.txt
```

### Step 2: Setup API Keys (Optional)
```bash
cp .env.example .env
# Edit .env and add your API keys:
# - GROQ_API_KEY (optional)
# - OPENAI_API_KEY (optional)
```

For **Local Llama** (no API key needed):
```bash
# Install Ollama from https://ollama.ai
ollama pull llama2
# Ollama runs automatically on localhost:11434
```

### Step 3: Run the Evaluator
```bash
# Web UI (Recommended)
streamlit run app.py

# Or command-line demo
python demo.py
```

## 🔧 What You Can Do

### 1. Compare Multiple Models
Evaluate the same problem with Groq, OpenAI GPT-4, and Local Llama 2 simultaneously to see which performs best.

### 2. Measure 15 Core Metrics
Get detailed scores on:
- Task Success Rate
- Pass@1 (Functional Correctness)
- Multi-File Edit Accuracy
- Planning Quality
- Tool Invocation Accuracy
- Context Retention
- Hallucination Rate
- Scope Control
- Code Quality
- Security Awareness
- Recovery Rate
- Latency per Step
- Token Efficiency
- Developer Intervention Rate
- Output Stability

### 3. Generate Automatic Test Cases
AI automatically creates test cases from problem statements.

### 4. Batch Evaluate
Test multiple models on multiple problems and export results.

### 5. Export & Report
Get results as JSON/CSV for further analysis.

## 🎯 Architecture Overview

### Core Components

1. **AgentEvaluator** (evaluator.py)
   - Main orchestrator
   - Manages multiple evaluations
   - Aggregates results
   - Exports reports

2. **ModelClient Classes** (model_clients.py)
   - GroqModelClient (cloud LLM, fast)
   - OpenAIModelClient (cloud LLM, high quality)
   - LlamaLocalClient (local LLM, free/private)

3. **MetricsScore** (evaluator.py)
   - 15 core metrics as data class
   - Calculation logic
   - Scoring functions

4. **Streamlit UI** (app.py)
   - Interactive evaluation
   - Model selection
   - Result visualization
   - Export functionality

## 📊 Understanding Metrics

| Category | Metrics |
|----------|---------|
| **Correctness** | Task Success, Pass@1 |
| **Quality** | Code Quality, Multi-File Accuracy |
| **Planning** | Planning Score, Tool Accuracy |
| **Memory** | Context Retention, Recovery Rate |
| **Safety** | Hallucination Rate, Scope Control, Security |
| **Performance** | Latency, Token Efficiency |
| **Reliability** | Intervention Rate, Output Stability |

**Lower is Better**: Hallucination, Intervention, Latency
**Higher is Better**: All other metrics

## 💡 Usage Examples

### Python Script Example
```python
from evaluator import AgentEvaluator, ModelType
from model_clients import GroqModelClient

# Setup
evaluator = AgentEvaluator()
groq = GroqModelClient()
evaluator.register_model(ModelType.GROQ, groq)

# Evaluate
result = evaluator.evaluate_task(
    task_id="sorting",
    problem_statement="Implement quicksort",
    language="python",
    model_type=ModelType.GROQ
)

# Results
print(f"Overall: {result.metrics.average()}/100")
evaluator.export_results("results.json")
```

### Web UI
Simply run `streamlit run app.py` and:
1. Select models from sidebar
2. Choose or write problem
3. Click "Run Evaluation"
4. Compare results and export

## 🔌 Supported Models

| Model | Type | Speed | Quality | Cost | Setup |
|-------|------|-------|---------|------|-------|
| Groq (Mixtral) | Cloud | ⚡⚡⚡ Fast | ⭐⭐⭐⭐ | 💰 Free | API key |
| OpenAI GPT-4 | Cloud | ⚡ Slow | ⭐⭐⭐⭐⭐ Best | 💰💰 $ | API key |
| Llama 2 (Ollama) | Local | ⚡ Slow | ⭐⭐⭐ Good | FREE | Ollama |

## ⚙️ Configuration

### Environment Variables (.env)
```
GROQ_API_KEY=gsk_...        # Optional
OPENAI_API_KEY=sk-...       # Optional
OLLAMA_BASE_URL=...         # Default: localhost:11434
NUM_TEST_RUNS=2             # Evaluation runs for stability
```

### Model Settings (in code)
```python
GroqModelClient(
    api_key="...",
    model_name="mixtral-8x7b-32768"
)

OpenAIModelClient(
    api_key="...",
    model_name="gpt-4"
)

LlamaLocalClient(
    model_name="llama2",
    base_url="http://localhost:11434"
)
```

## 🧪 Running Tests

```bash
# All tests
pytest test_evaluator.py -v

# Specific test class
pytest test_evaluator.py::TestMetricsScore -v

# With coverage
pytest test_evaluator.py --cov=evaluator
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Model not registered" | Check API keys in .env, verify internet |
| Ollama connection failed | Run `ollama serve`, ensure localhost:11434 |
| JSON parsing errors | Try shorter problem statement, use different model |
| Memory issues | Use Groq/OpenAI instead of local Llama |
| Tests fail | Run `pip install -r requirements.txt` again |

## 🚀 Next Steps

1. **Try the Web UI**
   ```bash
   streamlit run app.py
   ```
   Open browser to http://localhost:8501

2. **Run the Demo**
   ```bash
   python demo.py
   ```
   See example evaluation flow

3. **Evaluate Your Own Problem**
   - Use app.py or write custom Python script
   - Set task_id, problem_statement, language
   - Call evaluator.evaluate_task()

4. **Export & Analyze Results**
   - Results auto-exported to JSON/CSV
   - Compare models side-by-side
   - Track metrics over time

## 📈 Roadmap

**Future Features:**
- Benchmark dataset (100+ problems)
- Real-time metrics dashboard
- GitHub CI/CD integration
- Additional model providers (Anthropic, Claude)
- Cost analysis per model
- Custom metrics builder
- Regression testing suite

## 🤝 Extending the Framework

### Add Custom Model
```python
class CustomModelClient(ModelClient):
    def generate_test_cases(self, problem, language, num_cases=5):
        # Your logic
        pass
    # ... implement other methods
```

### Add Custom Metric
Edit `MetricsScore` class in `evaluator.py` and update calculation logic.

### Add Test Cases
Add test classes to `test_evaluator.py`.

## 📞 Support Resources

- **README.md**: Full feature documentation
- **SETUP.md**: Configuration & troubleshooting
- **demo.py**: Working code examples
- **test_evaluator.py**: Usage patterns in tests
- **Inline docstrings**: Every class and function documented

## 🎓 Learning Path

1. **Start**: Read README.md overview
2. **Setup**: Follow SETUP.md configuration
3. **Try**: Run demo.py to see examples
4. **Explore**: Open app.py in Streamlit
5. **Extend**: Modify evaluator.py for custom needs
6. **Test**: Use test_evaluator.py as reference

## ✨ Key Features Summary

✅ **Multi-Model Support** - Compare Groq, OpenAI, Llama
✅ **15 Core Metrics** - Comprehensive evaluation
✅ **Automatic Test Generation** - AI-generated test cases
✅ **Web UI** - Streamlit dashboard
✅ **Batch Evaluation** - Evaluate multiple models/tasks
✅ **Export & Reporting** - JSON/CSV export
✅ **Stability Testing** - Multiple runs for consistency
✅ **Well-Tested** - Unit & integration tests
✅ **Production Ready** - Error handling, logging
✅ **Fully Documented** - Docstrings, guides, examples

## 📄 License

MIT License - Use freely in your projects

---

**Created**: January 2026
**Version**: 1.0.0
**Status**: Ready to use

For questions, check the documentation files or review the code comments!
