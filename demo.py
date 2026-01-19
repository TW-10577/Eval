"""
Example usage and testing of the AI Code Evaluator
"""

from evaluator import AgentEvaluator, ModelType
from model_clients import GroqModelClient, OpenAIModelClient, LlamaLocalClient
import json


def demo_evaluate_models():
    """Demo: Evaluate same task across different models"""
    
    # Initialize evaluator
    evaluator = AgentEvaluator()
    
    # Example coding problem
    problem = """
    Write a function to find the longest palindromic substring in a string.
    
    Example:
    Input: "babad"
    Output: "bab" or "aba"
    
    Constraints:
    - String length up to 1000
    - Case sensitive
    - Return one palindrome if multiple exist
    """
    
    # Register model clients
    print("🔧 Registering model clients...")
    
    # Try to register Groq if API key available
    try:
        groq_client = GroqModelClient()
        evaluator.register_model(ModelType.GROQ, groq_client)
        print("✅ Groq registered")
    except Exception as e:
        print(f"⚠️  Groq not available: {e}")
    
    # Try to register OpenAI if API key available
    try:
        openai_client = OpenAIModelClient()
        evaluator.register_model(ModelType.OPENAI, openai_client)
        print("✅ OpenAI registered")
    except Exception as e:
        print(f"⚠️  OpenAI not available: {e}")
    
    # Try to register Llama if Ollama running
    try:
        llama_client = LlamaLocalClient(model_name="llama2")
        evaluator.register_model(ModelType.LLAMA_LOCAL, llama_client)
        print("✅ Llama (local) registered")
    except Exception as e:
        print(f"⚠️  Llama not available: {e}")
    
    # Evaluate task with each model
    print("\n📊 Evaluating task across models...")
    
    results = {}
    for model_type in evaluator.model_clients.keys():
        print(f"\n🚀 Evaluating with {model_type.value}...")
        result = evaluator.evaluate_task(
            task_id="task_001",
            problem_statement=problem,
            language="python",
            model_type=model_type,
            num_test_runs=2
        )
        
        results[result.model_name] = result
        print(f"   Status: {result.status.value}")
        print(f"   Average Score: {result.metrics.average():.1f}/100")
    
    # Generate comparison
    print("\n📈 Model Comparison:")
    print("=" * 60)
    
    comparison = evaluator.compare_models("task_001")
    for model_name, model_data in comparison["models"].items():
        print(f"\n{model_name}:")
        print(f"  Overall Score: {model_data['average_score']:.1f}/100")
        metrics = model_data['metrics']
        print(f"  Task Success Rate: {metrics['task_success_rate']:.1f}%")
        print(f"  Code Quality: {metrics['code_quality_score']:.1f}/100")
        print(f"  Context Retention: {metrics['context_retention']:.1f}%")
        print(f"  Hallucination Rate: {metrics['hallucination_rate']:.1f}%")
    
    # Export results
    print("\n💾 Exporting results...")
    evaluator.export_results("evaluation_results.json")
    print("✅ Results saved to evaluation_results.json")
    
    # Get summary
    summary = evaluator.get_summary_report()
    print("\n📋 Summary Report:")
    print(json.dumps(summary, indent=2))


def demo_single_model_evaluation():
    """Demo: Evaluate single model on multiple tasks"""
    
    evaluator = AgentEvaluator()
    
    # Register Groq as example
    try:
        groq_client = GroqModelClient()
        evaluator.register_model(ModelType.GROQ, groq_client)
    except:
        print("Groq not available")
        return
    
    tasks = [
        {
            "id": "task_palindrome",
            "problem": "Find the longest palindromic substring",
            "language": "python"
        },
        {
            "id": "task_fibonacci",
            "problem": "Calculate fibonacci number at position n with memoization",
            "language": "python"
        },
        {
            "id": "task_bfs",
            "problem": "Implement BFS algorithm for graph traversal",
            "language": "python"
        }
    ]
    
    print("📚 Evaluating multiple tasks with single model...")
    print("=" * 60)
    
    for task in tasks:
        print(f"\n🔍 Evaluating: {task['id']}")
        result = evaluator.evaluate_task(
            task_id=task['id'],
            problem_statement=task['problem'],
            language=task['language'],
            model_type=ModelType.GROQ,
            num_test_runs=1
        )
        print(f"   Score: {result.metrics.average():.1f}/100")
    
    # Summary
    summary = evaluator.get_summary_report()
    print("\n📊 Overall Performance Summary:")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    print("🤖 AI Coding Agent Evaluator\n")
    
    # Uncomment the demo you want to run:
    demo_evaluate_models()
    # demo_single_model_evaluation()
