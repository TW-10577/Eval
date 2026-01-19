#!/usr/bin/env python3
"""
Quick Reference Commands for AI Code Evaluator

Copy these commands to your terminal to get started quickly!
"""

# ============================================================================
# INSTALLATION
# ============================================================================

# 1. Install all dependencies
pip install -r requirements.txt

# 2. Setup environment variables
cp .env.example .env
# Then edit .env and add your API keys

# ============================================================================
# RUNNING THE APPLICATION
# ============================================================================

# Start the Streamlit web interface (Recommended)
streamlit run app.py

# Run command-line demo
python demo.py

# Run unit tests
pytest test_evaluator.py -v

# ============================================================================
# PYTHON USAGE EXAMPLES
# ============================================================================

# Example 1: Evaluate with single model (Groq)
python3 << 'EOF'
from evaluator import AgentEvaluator, ModelType
from model_clients import GroqModelClient

evaluator = AgentEvaluator()
groq = GroqModelClient()
evaluator.register_model(ModelType.GROQ, groq)

result = evaluator.evaluate_task(
    task_id="test",
    problem_statement="Write a function to reverse a string",
    language="python",
    model_type=ModelType.GROQ
)

print(f"Score: {result.metrics.average():.1f}/100")
evaluator.export_results("results.json")
EOF

# Example 2: Compare multiple models
python3 << 'EOF'
from evaluator import AgentEvaluator, ModelType
from model_clients import GroqModelClient, OpenAIModelClient, LlamaLocalClient

evaluator = AgentEvaluator()

try:
    evaluator.register_model(ModelType.GROQ, GroqModelClient())
    print("✅ Groq registered")
except: print("⚠️ Groq unavailable")

try:
    evaluator.register_model(ModelType.OPENAI, OpenAIModelClient())
    print("✅ OpenAI registered")
except: print("⚠️ OpenAI unavailable")

try:
    evaluator.register_model(ModelType.LLAMA_LOCAL, LlamaLocalClient())
    print("✅ Llama registered")
except: print("⚠️ Llama unavailable")

problem = "Implement quicksort algorithm"

for model_type in evaluator.model_clients.keys():
    result = evaluator.evaluate_task(
        task_id="sorting",
        problem_statement=problem,
        language="python",
        model_type=model_type,
        num_test_runs=1
    )
    print(f"{result.model_name}: {result.metrics.average():.1f}/100")

evaluator.export_results("comparison.json")
EOF

# Example 3: Batch evaluate multiple tasks
python3 << 'EOF'
from evaluator import AgentEvaluator, ModelType
from model_clients import GroqModelClient

evaluator = AgentEvaluator()
groq = GroqModelClient()
evaluator.register_model(ModelType.GROQ, groq)

tasks = [
    ("palindrome", "Find longest palindromic substring"),
    ("fibonacci", "Calculate fibonacci with memoization"),
    ("bfs", "Implement BFS graph traversal"),
]

for task_id, problem in tasks:
    result = evaluator.evaluate_task(
        task_id=task_id,
        problem_statement=problem,
        language="python",
        model_type=ModelType.GROQ,
        num_test_runs=2
    )
    print(f"{task_id}: {result.metrics.average():.1f}/100")

summary = evaluator.get_summary_report()
print(f"\nTotal evaluations: {summary['total_evaluations']}")
EOF

# ============================================================================
# SETUP LOCAL LLAMA (OLLAMA)
# ============================================================================

# Install Ollama (one-time setup)
# Linux: curl -fsSL https://ollama.ai/install.sh | sh
# Or download from https://ollama.ai

# Start Ollama server
ollama serve

# In another terminal, download model
ollama pull llama2

# Verify setup (should show "success")
python3 -c "from model_clients import LlamaLocalClient; c = LlamaLocalClient(); print('✅ Ollama ready')" 2>/dev/null || echo "⚠️ Ollama not running"

# ============================================================================
# API KEY SETUP
# ============================================================================

# Get Groq API Key
# 1. Go to https://console.groq.com
# 2. Create account / login
# 3. Create API key
# 4. Copy to .env: GROQ_API_KEY=gsk_...

# Get OpenAI API Key
# 1. Go to https://platform.openai.com/api-keys
# 2. Create new secret key
# 3. Copy to .env: OPENAI_API_KEY=sk-...

# ============================================================================
# METRICS EXPLAINED
# ============================================================================

"""
15 Core Metrics:

1. Task Success Rate (0-100%)
   → Percentage of tasks completed correctly

2. Pass@1 (0-100%)
   → Probability first solution passes all tests

3. Multi-File Edit Accuracy (0-100%)
   → Correctness of changes across files

4. Planning Quality Score (0-100)
   → Quality of task decomposition

5. Tool Invocation Accuracy (0-100%)
   → Correct usage of tools

6. Context Retention (0-100%)
   → Memory of prior steps/constraints

7. Hallucination Rate (0-100%, lower is better)
   → Frequency of invented APIs/files

8. Scope Control (0-100%)
   → Avoids unnecessary changes

9. Code Quality Score (0-100)
   → Readability, structure, maintainability

10. Security Awareness (0-100%)
    → Detection of insecure patterns

11. Recovery Rate (0-100%)
    → Self-correction capability

12. Latency per Step (seconds, lower is better)
    → Time per reasoning step

13. Token Efficiency (tokens, lower is better)
    → Tokens consumed per task

14. Developer Intervention Rate (0-100%, lower is better)
    → How often human intervention needed

15. Output Stability (0-100%)
    → Consistency across runs
"""

# ============================================================================
# FILE STRUCTURE
# ============================================================================

"""
eval/
├── evaluator.py              # Core engine + 15 metrics
├── model_clients.py          # Groq, OpenAI, Llama clients
├── app.py                    # Streamlit web UI
├── demo.py                   # Example usage
├── test_evaluator.py         # Unit tests
├── requirements.txt          # Dependencies
├── .env.example              # Environment template
├── README.md                 # Full documentation
├── SETUP.md                  # Configuration guide
└── GETTING_STARTED.md        # Quick start guide
"""

# ============================================================================
# COMMON ISSUES & FIXES
# ============================================================================

# Issue: "GROQ_API_KEY not found"
# Fix: Create .env file with GROQ_API_KEY=your_key

# Issue: Ollama connection error
# Fix: Run "ollama serve" in another terminal first

# Issue: JSON parsing error
# Fix: Problem statement too long, use shorter description

# Issue: Memory error with Llama
# Fix: Use Groq/OpenAI instead, or get more VRAM

# Issue: Tests fail
# Fix: pip install -r requirements.txt --upgrade

# ============================================================================
# USEFUL COMMANDS
# ============================================================================

# Check all evaluations completed
python3 -c "import json; print(json.load(open('evaluation_results.json')))" | head -20

# View summary report
python3 -c "from evaluator import AgentEvaluator; e = AgentEvaluator(); import json; print(json.dumps(e.get_summary_report(), indent=2))"

# Run tests with coverage
pytest test_evaluator.py --cov=evaluator --cov-report=html

# Format code
python3 -m black evaluator.py model_clients.py app.py demo.py

# Check for errors
python3 -m py_compile *.py

# ============================================================================
# NEXT STEPS
# ============================================================================

# 1. Install dependencies:
#    pip install -r requirements.txt

# 2. Setup API keys:
#    cp .env.example .env
#    (edit .env with your keys)

# 3. Run web UI:
#    streamlit run app.py

# 4. Or run demo:
#    python demo.py

# 5. Check documentation:
#    - README.md (features)
#    - SETUP.md (detailed setup)
#    - GETTING_STARTED.md (quick start)
#    - evaluator.py docstrings (code reference)

# ============================================================================
# SUPPORT
# ============================================================================

# For questions or issues:
# 1. Check README.md for feature docs
# 2. Check SETUP.md for troubleshooting
# 3. Look at demo.py for code examples
# 4. Review docstrings in evaluator.py
# 5. Run tests: pytest test_evaluator.py -v

# ============================================================================
# END OF QUICK REFERENCE
# ============================================================================
