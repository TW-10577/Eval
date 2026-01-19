# AI Coding Agent Evaluator - Project Index

## 📋 Complete Project Documentation

Welcome to the **AI Coding Agent Evaluator** - a comprehensive framework for evaluating and comparing AI coding assistants using **15 core metrics** across **multiple model types** (Groq, OpenAI, Local Llama).

---

## 🗂️ File Guide

### 📚 Documentation Files (Read These First!)

| File | Purpose | Audience |
|------|---------|----------|
| **[README.md](README.md)** | Complete feature overview and usage guide | Everyone |
| **[GETTING_STARTED.md](GETTING_STARTED.md)** | Quick start guide with 3-step setup | New users |
| **[SETUP.md](SETUP.md)** | Detailed configuration, troubleshooting, examples | Setup help |
| **[QUICK_START.py](QUICK_START.py)** | Copy-paste commands and code examples | Quick reference |

### 💻 Source Code Files

| File | Lines | Purpose | Key Classes |
|------|-------|---------|-------------|
| **[evaluator.py](evaluator.py)** | 400+ | Core evaluation engine with 15 metrics | `AgentEvaluator`, `MetricsScore`, `EvaluationResult` |
| **[model_clients.py](model_clients.py)** | 350+ | LLM client implementations | `GroqModelClient`, `OpenAIModelClient`, `LlamaLocalClient` |
| **[app.py](app.py)** | 400+ | Streamlit web interface | Streamlit components |
| **[demo.py](demo.py)** | 150+ | Working code examples | Example functions |

### 🧪 Testing & Configuration

| File | Purpose |
|------|---------|
| **[test_evaluator.py](test_evaluator.py)** | Unit & integration tests (pytest) |
| **[requirements.txt](requirements.txt)** | Python dependencies |
| **[.env.example](.env.example)** | Environment variable template |

---

## 🎯 The 15 Core Metrics

### Understanding Metrics by Category

**Correctness & Functionality**
- 1️⃣ Task Success Rate (%)
- 2️⃣ Pass@1 (%)

**Code Quality**
- 3️⃣ Multi-File Edit Accuracy (%)
- 9️⃣ Code Quality Score (0-100)

**Planning & Problem Solving**
- 4️⃣ Planning Quality Score (0-100)
- 5️⃣ Tool Invocation Accuracy (%)

**Memory & Self-Correction**
- 6️⃣ Context Retention (%)
- 1️⃣1️⃣ Recovery/Self-Correction Rate (%)

**Safety & Security**
- 7️⃣ Hallucination Rate (%, lower is better)
- 8️⃣ Scope Control (%)
- 🔟 Security Awareness (%)

**Efficiency**
- 1️⃣2️⃣ Latency per Step (seconds, lower is better)
- 1️⃣3️⃣ Token Efficiency (tokens, lower is better)

**Consistency & Reliability**
- 1️⃣4️⃣ Developer Intervention Rate (%, lower is better)
- 1️⃣5️⃣ Output Stability (%)

---

## 🚀 Quick Start (5 Minutes)

### 1. Install
```bash
cd /home/tw10577/eval
pip install -r requirements.txt
```

### 2. Configure (Optional - only for cloud models)
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Run
```bash
# Web UI (Recommended)
streamlit run app.py

# OR Command-line
python demo.py
```

**That's it!** Start evaluating models.

---

## 🎓 Learning Paths

### For First-Time Users
1. Read [GETTING_STARTED.md](GETTING_STARTED.md) (5 min)
2. Follow installation in [SETUP.md](SETUP.md) (5 min)
3. Run `streamlit run app.py` (5 min)
4. Test with web UI (10 min)

### For Python Developers
1. Skim [README.md](README.md) overview
2. Check code examples in [QUICK_START.py](QUICK_START.py)
3. Review [demo.py](demo.py) for patterns
4. Explore [evaluator.py](evaluator.py) source code
5. Run tests: `pytest test_evaluator.py -v`

### For Integration/Advanced Users
1. Review [evaluator.py](evaluator.py) class design
2. Understand `AgentEvaluator` and `MetricsScore`
3. Check [model_clients.py](model_clients.py) for client patterns
4. Extend by creating custom model clients
5. Add custom metrics to `MetricsScore`

### For DevOps/Deployment
1. Check [requirements.txt](requirements.txt) for dependencies
2. Review [SETUP.md](SETUP.md) environment variables
3. Configure API keys in production
4. Run tests: `pytest test_evaluator.py`
5. Deploy [app.py](app.py) with Streamlit

---

## 📖 Key Concepts

### The AgentEvaluator Class
The main orchestrator that:
- Manages model clients
- Runs evaluations
- Aggregates metrics
- Exports results

```python
from evaluator import AgentEvaluator, ModelType
from model_clients import GroqModelClient

evaluator = AgentEvaluator()
groq = GroqModelClient()
evaluator.register_model(ModelType.GROQ, groq)

result = evaluator.evaluate_task(...)
summary = evaluator.get_summary_report()
```

### The MetricsScore Class
15 numeric values representing performance across key dimensions:
- Range: 0-100 (or specific scales for latency/tokens)
- `average()` method calculates overall score
- `to_dict()` converts to JSON-serializable format

### Model Clients
Three implementations for different LLM backends:
- **GroqModelClient**: Fast cloud LLM
- **OpenAIModelClient**: High-quality cloud LLM
- **LlamaLocalClient**: Free local LLM via Ollama

Each implements:
- `generate_test_cases()`: AI-generated test cases
- `evaluate_code()`: Quality assessment
- `analyze_planning()`: Task decomposition analysis

---

## 🔗 File Dependency Map

```
app.py (Streamlit UI)
    ↓ imports
evaluator.py + model_clients.py
    ↓
    Uses ModelClient classes
    ↓
    Groq API / OpenAI API / Ollama

demo.py (Examples)
    ↓ imports
evaluator.py + model_clients.py

test_evaluator.py (Tests)
    ↓ imports
evaluator.py
    ↓
    Uses mock clients for testing
```

---

## 💡 Common Use Cases

### Use Case 1: Compare Models on One Problem
```python
# See: demo.py - demo_evaluate_models()
# Evaluate same problem with Groq, OpenAI, Llama
evaluator.evaluate_task(..., model_type=ModelType.GROQ)
evaluator.evaluate_task(..., model_type=ModelType.OPENAI)
evaluator.evaluate_task(..., model_type=ModelType.LLAMA_LOCAL)
```

### Use Case 2: Evaluate One Model on Many Problems
```python
# See: demo.py - demo_single_model_evaluation()
for task in tasks:
    evaluator.evaluate_task(..., model_type=ModelType.GROQ)
```

### Use Case 3: CI/CD Integration Testing
```python
# Evaluate AI assistant quality as part of pipeline
# Export JSON results for analysis
evaluator.export_results("ci_results.json")
```

### Use Case 4: Interactive Comparison
```bash
# Use web UI for point-and-click comparison
streamlit run app.py
```

---

## 🔧 Extension Points

### Add a New Model
Extend `ModelClient` in `model_clients.py`:
```python
class MyModelClient(ModelClient):
    def generate_test_cases(self, ...): pass
    def evaluate_code(self, ...): pass
    def analyze_planning(self, ...): pass
```

### Add a New Metric
Edit `MetricsScore` dataclass in `evaluator.py` and update aggregation logic.

### Customize Evaluation Flow
Extend `AgentEvaluator` in `evaluator.py` and override evaluation methods.

---

## 📊 Understanding Results

### Result Object Structure
```python
EvaluationResult {
    task_id: "task_001",
    model_type: ModelType.GROQ,
    model_name: "Groq Mixtral",
    status: TaskStatus.SUCCESS,
    metrics: MetricsScore,  # 15 values
    timestamp: "2026-01-19T...",
    execution_time: 5.2,    # seconds
}
```

### Metrics Range
- Most metrics: 0-100 (higher is better)
- Hallucination: 0-100 (lower is better)
- Intervention: 0-100 (lower is better)
- Latency: seconds (lower is better)
- Tokens: count (lower is better)

### Overall Score
Calculated by `metrics.average()`:
- Averages 13 of 15 metrics (excludes latency/tokens)
- Returns 0-100 score
- Higher is better

---

## 🧪 Testing

### Run All Tests
```bash
cd /home/tw10577/eval
pytest test_evaluator.py -v
```

### Run Specific Test
```bash
pytest test_evaluator.py::TestMetricsScore -v
```

### Run with Coverage
```bash
pytest test_evaluator.py --cov=evaluator
```

### Test Categories
- **TestMetricsScore**: Metric calculation
- **TestEvaluationResult**: Result structure
- **TestAgentEvaluator**: Main orchestrator
- **TestIntegration**: Full pipeline

---

## 🐛 Troubleshooting Quick Links

| Issue | Solution | File |
|-------|----------|------|
| API key not found | Check .env file | [SETUP.md](SETUP.md) |
| Ollama connection error | Start ollama server | [SETUP.md](SETUP.md) |
| Model not available | Register client first | [demo.py](demo.py) |
| JSON parsing error | Try shorter problem | [SETUP.md](SETUP.md) |
| Memory error | Use cloud models | [SETUP.md](SETUP.md) |
| Tests failing | Reinstall requirements | [test_evaluator.py](test_evaluator.py) |

---

## 📞 Documentation Index by Topic

| Topic | Files |
|-------|-------|
| **Getting Started** | GETTING_STARTED.md, QUICK_START.py |
| **Setup & Config** | SETUP.md, .env.example |
| **Usage Examples** | demo.py, QUICK_START.py |
| **API Reference** | evaluator.py, model_clients.py (docstrings) |
| **Testing** | test_evaluator.py |
| **Web UI** | app.py |
| **Features** | README.md |

---

## 🎯 Next Steps

1. **Choose your path:**
   - Web UI user? → `streamlit run app.py`
   - Python developer? → Check `demo.py` examples
   - Integration? → Review `evaluator.py` API

2. **Get credentials** (optional):
   - Groq: https://console.groq.com
   - OpenAI: https://platform.openai.com
   - Llama: `ollama pull llama2` (free!)

3. **Start evaluating:**
   - Define your coding problem
   - Select models to test
   - Run evaluation
   - Compare results

4. **Explore features:**
   - Generate test cases
   - Measure 15 metrics
   - Compare models
   - Export results

---

## 📄 Project Stats

| Metric | Value |
|--------|-------|
| **Total Python Code** | 1400+ lines |
| **Core Engine** | evaluator.py (400 lines) |
| **Model Clients** | model_clients.py (350 lines) |
| **Web UI** | app.py (400 lines) |
| **Tests** | test_evaluator.py (300+ lines) |
| **Documentation** | 2000+ lines across files |
| **Metrics Tracked** | 15 core metrics |
| **Model Support** | 3+ (Groq, OpenAI, Llama) |
| **Features** | 10+ major features |

---

## ✨ Key Features

✅ Multi-model support (Groq, OpenAI, Llama)
✅ 15 comprehensive evaluation metrics
✅ Automatic test case generation
✅ Web UI with Streamlit
✅ Batch evaluation capability
✅ JSON/CSV export
✅ Detailed reporting
✅ Unit tests included
✅ Production-ready code
✅ Fully documented

---

## 🎓 Version & Status

**Version:** 1.0.0
**Status:** Production Ready
**Created:** January 2026
**License:** MIT

---

## 🙋 Need Help?

1. **Getting started?** → Read [GETTING_STARTED.md](GETTING_STARTED.md)
2. **Setup issues?** → Check [SETUP.md](SETUP.md)
3. **Code examples?** → See [QUICK_START.py](QUICK_START.py)
4. **Features?** → Review [README.md](README.md)
5. **API details?** → Check source code docstrings
6. **Running tests?** → `pytest test_evaluator.py -v`

---

**Ready to evaluate AI coding agents? Start with `streamlit run app.py` or `python demo.py`** 🚀
