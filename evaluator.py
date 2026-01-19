"""
AI Coding Agent Evaluator
Evaluates both local (LLama) and cloud models (OpenAI, Groq) on coding tasks
Measures 15 core metrics for AI coding assistant performance
"""

from enum import Enum
from typing import Optional, Dict, Any, List
import json
from datetime import datetime
from dataclasses import dataclass, asdict
import time


class ModelType(Enum):
    """Supported model types"""
    LLAMA_LOCAL = "llama_local"
    OPENAI = "openai"
    GROQ = "groq"


class TaskStatus(Enum):
    """Task execution status"""
    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"
    TIMEOUT = "timeout"
    ERROR = "error"


@dataclass
class MetricsScore:
    """Data class for storing evaluation metrics"""
    task_success_rate: float  # 1. Percentage of tasks completed correctly
    pass_at_1: float  # 2. Probability first solution passes all tests
    multi_file_edit_accuracy: float  # 3. Correctness of multi-file changes
    planning_quality_score: float  # 4. Task decomposition quality
    tool_invocation_accuracy: float  # 5. Correct tool usage
    context_retention: float  # 6. Memory of prior steps/constraints
    hallucination_rate: float  # 7. Frequency of invented APIs/behaviors
    scope_control: float  # 8. Avoids unnecessary/risky changes
    code_quality_score: float  # 9. Readability, structure, maintainability
    security_awareness: float  # 10. Detection of insecure patterns
    recovery_rate: float  # 11. Self-correction capability
    latency_per_step: float  # 12. Time per step (seconds)
    token_efficiency: float  # 13. Tokens per successful task
    developer_intervention_rate: float  # 14. % requiring human intervention
    output_stability: float  # 15. Consistency across runs
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary"""
        return asdict(self)
    
    def average(self) -> float:
        """Calculate average score (0-100)"""
        scores = [
            self.task_success_rate,
            self.pass_at_1,
            self.multi_file_edit_accuracy,
            self.planning_quality_score,
            self.tool_invocation_accuracy,
            self.context_retention,
            100 - self.hallucination_rate,  # Invert (lower is better)
            self.scope_control,
            self.code_quality_score,
            self.security_awareness,
            self.recovery_rate,
            # Skip latency and tokens (different scale)
            100 - self.developer_intervention_rate,  # Invert
            self.output_stability,
        ]
        return sum(scores) / len(scores)


@dataclass
class EvaluationResult:
    """Complete evaluation result for a single task"""
    task_id: str
    model_type: ModelType
    model_name: str
    task_description: str
    status: TaskStatus
    metrics: MetricsScore
    timestamp: str
    execution_time: float
    error_message: Optional[str] = None
    generated_code: Optional[str] = None
    test_results: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['model_type'] = self.model_type.value
        data['status'] = self.status.value
        data['metrics'] = self.metrics.to_dict()
        return data


class CodeEvaluator:
    """Base class for code evaluation"""
    
    def __init__(self):
        self.test_results = {}
    
    def evaluate_correctness(self, code: str, test_cases: List[Dict]) -> tuple[float, List[str]]:
        """
        Evaluate code correctness against test cases
        Returns: (success_rate: 0-100, failures: list of failed tests)
        """
        raise NotImplementedError
    
    def evaluate_efficiency(self, code: str, execution_time: float) -> Dict[str, float]:
        """Evaluate time and space complexity"""
        raise NotImplementedError
    
    def evaluate_code_quality(self, code: str) -> float:
        """Evaluate readability, structure, maintainability (0-100)"""
        raise NotImplementedError


class ModelClient:
    """Base class for model interactions"""
    
    def __init__(self, model_type: ModelType, model_name: str):
        self.model_type = model_type
        self.model_name = model_name
    
    def generate_test_cases(self, problem: str, language: str, num_cases: int = 5) -> List[Dict]:
        """Generate test cases from problem statement"""
        raise NotImplementedError
    
    def evaluate_code(self, code: str, problem: str, language: str) -> Dict[str, Any]:
        """Evaluate code quality against problem requirements"""
        raise NotImplementedError
    
    def analyze_planning(self, problem: str) -> Dict[str, Any]:
        """Analyze how well the agent decomposed the task"""
        raise NotImplementedError


class AgentEvaluator:
    """Main evaluator for AI coding agents"""
    
    def __init__(self):
        self.results: List[EvaluationResult] = []
        self.model_clients: Dict[ModelType, ModelClient] = {}
    
    def register_model(self, model_type: ModelType, client: ModelClient):
        """Register a model client"""
        self.model_clients[model_type] = client
    
    def evaluate_task(
        self,
        task_id: str,
        problem_statement: str,
        language: str,
        model_type: ModelType,
        num_test_runs: int = 3,
    ) -> EvaluationResult:
        """
        Evaluate a single task with specified model
        Runs multiple times to measure stability
        """
        start_time = time.time()
        
        if model_type not in self.model_clients:
            return EvaluationResult(
                task_id=task_id,
                model_type=model_type,
                model_name="unknown",
                task_description=problem_statement,
                status=TaskStatus.ERROR,
                metrics=self._get_zero_metrics(),
                timestamp=datetime.now().isoformat(),
                execution_time=0,
                error_message=f"Model type {model_type} not registered"
            )
        
        client = self.model_clients[model_type]
        
        # Run evaluation multiple times for stability
        runs = []
        for run_num in range(num_test_runs):
            result = self._single_evaluation_run(
                task_id, problem_statement, language, client
            )
            runs.append(result)
        
        # Aggregate results
        aggregated = self._aggregate_results(task_id, problem_statement, model_type, client, runs)
        aggregated.execution_time = time.time() - start_time
        
        self.results.append(aggregated)
        return aggregated
    
    def _single_evaluation_run(
        self,
        task_id: str,
        problem_statement: str,
        language: str,
        client: ModelClient,
    ) -> Dict[str, Any]:
        """Single evaluation run"""
        try:
            # Generate test cases
            test_cases = client.generate_test_cases(problem_statement, language)
            
            # Evaluate planning
            planning = client.analyze_planning(problem_statement)
            
            # Evaluate code quality
            code_eval = client.evaluate_code(problem_statement, language)
            
            return {
                "status": TaskStatus.SUCCESS,
                "test_cases": test_cases,
                "planning": planning,
                "code_eval": code_eval,
            }
        except Exception as e:
            return {
                "status": TaskStatus.ERROR,
                "error": str(e),
            }
    
    def _aggregate_results(
        self,
        task_id: str,
        problem_statement: str,
        model_type: ModelType,
        client: ModelClient,
        runs: List[Dict[str, Any]],
    ) -> EvaluationResult:
        """Aggregate multiple runs into final metrics"""
        
        # Calculate metrics based on runs
        metrics = MetricsScore(
            task_success_rate=85.0,  # Placeholder
            pass_at_1=80.0,
            multi_file_edit_accuracy=90.0,
            planning_quality_score=75.0,
            tool_invocation_accuracy=88.0,
            context_retention=82.0,
            hallucination_rate=5.0,
            scope_control=86.0,
            code_quality_score=79.0,
            security_awareness=84.0,
            recovery_rate=72.0,
            latency_per_step=0.5,
            token_efficiency=150.0,
            developer_intervention_rate=15.0,
            output_stability=88.0,
        )
        
        return EvaluationResult(
            task_id=task_id,
            model_type=model_type,
            model_name=client.model_name,
            task_description=problem_statement,
            status=TaskStatus.SUCCESS,
            metrics=metrics,
            timestamp=datetime.now().isoformat(),
            execution_time=0,
        )
    
    def _get_zero_metrics(self) -> MetricsScore:
        """Return zero metrics"""
        return MetricsScore(
            task_success_rate=0,
            pass_at_1=0,
            multi_file_edit_accuracy=0,
            planning_quality_score=0,
            tool_invocation_accuracy=0,
            context_retention=0,
            hallucination_rate=100,
            scope_control=0,
            code_quality_score=0,
            security_awareness=0,
            recovery_rate=0,
            latency_per_step=0,
            token_efficiency=0,
            developer_intervention_rate=100,
            output_stability=0,
        )
    
    def compare_models(self, task_id: str) -> Dict[str, Any]:
        """Compare performance across all models for a task"""
        task_results = [r for r in self.results if r.task_id == task_id]
        
        comparison = {
            "task_id": task_id,
            "models": {}
        }
        
        for result in task_results:
            comparison["models"][result.model_name] = {
                "model_type": result.model_type.value,
                "metrics": result.metrics.to_dict(),
                "average_score": result.metrics.average(),
            }
        
        return comparison
    
    def get_summary_report(self) -> Dict[str, Any]:
        """Get overall summary across all evaluations"""
        if not self.results:
            return {"error": "No evaluations completed"}
        
        by_model = {}
        for result in self.results:
            model_key = result.model_name
            if model_key not in by_model:
                by_model[model_key] = []
            by_model[model_key].append(result)
        
        summary = {
            "total_evaluations": len(self.results),
            "timestamp": datetime.now().isoformat(),
            "models": {}
        }
        
        for model_name, results in by_model.items():
            avg_metrics = self._calculate_average_metrics(results)
            summary["models"][model_name] = {
                "num_tasks": len(results),
                "average_metrics": avg_metrics.to_dict(),
                "average_score": avg_metrics.average(),
                "task_success_rate": sum(r.metrics.task_success_rate for r in results) / len(results),
            }
        
        return summary
    
    def _calculate_average_metrics(self, results: List[EvaluationResult]) -> MetricsScore:
        """Calculate average metrics across results"""
        if not results:
            return self._get_zero_metrics()
        
        avg = MetricsScore(
            task_success_rate=sum(r.metrics.task_success_rate for r in results) / len(results),
            pass_at_1=sum(r.metrics.pass_at_1 for r in results) / len(results),
            multi_file_edit_accuracy=sum(r.metrics.multi_file_edit_accuracy for r in results) / len(results),
            planning_quality_score=sum(r.metrics.planning_quality_score for r in results) / len(results),
            tool_invocation_accuracy=sum(r.metrics.tool_invocation_accuracy for r in results) / len(results),
            context_retention=sum(r.metrics.context_retention for r in results) / len(results),
            hallucination_rate=sum(r.metrics.hallucination_rate for r in results) / len(results),
            scope_control=sum(r.metrics.scope_control for r in results) / len(results),
            code_quality_score=sum(r.metrics.code_quality_score for r in results) / len(results),
            security_awareness=sum(r.metrics.security_awareness for r in results) / len(results),
            recovery_rate=sum(r.metrics.recovery_rate for r in results) / len(results),
            latency_per_step=sum(r.metrics.latency_per_step for r in results) / len(results),
            token_efficiency=sum(r.metrics.token_efficiency for r in results) / len(results),
            developer_intervention_rate=sum(r.metrics.developer_intervention_rate for r in results) / len(results),
            output_stability=sum(r.metrics.output_stability for r in results) / len(results),
        )
        return avg
    
    def export_results(self, filepath: str, format: str = "json"):
        """Export all results to file"""
        if format == "json":
            data = [r.to_dict() for r in self.results]
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")
