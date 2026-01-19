"""
Unit tests for the evaluator framework
"""

import pytest
import json
from datetime import datetime

from evaluator import (
    AgentEvaluator,
    ModelType,
    TaskStatus,
    MetricsScore,
    EvaluationResult,
)


class MockModelClient:
    """Mock model client for testing"""
    
    def __init__(self, model_name: str = "test-model"):
        self.model_name = model_name
        self.model_type = ModelType.GROQ
    
    def generate_test_cases(self, problem: str, language: str, num_cases: int = 5):
        return [
            {"input": "test1", "expected_output": "output1", "description": "Test 1"},
            {"input": "test2", "expected_output": "output2", "description": "Test 2"},
        ]
    
    def evaluate_code(self, code: str, problem: str, language: str):
        return {
            "correctness": 85,
            "efficiency": 80,
            "readability": 90,
            "robustness": 75,
            "maintainability": 85,
        }
    
    def analyze_planning(self, problem: str):
        return {
            "steps": ["Step 1", "Step 2", "Step 3"],
            "complexity": 7,
            "edge_cases": ["Edge case 1", "Edge case 2"],
            "planning_score": 80,
        }


class TestMetricsScore:
    """Test metrics calculation"""
    
    def test_metrics_to_dict(self):
        metrics = MetricsScore(
            task_success_rate=85.0,
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
        
        metrics_dict = metrics.to_dict()
        assert metrics_dict['task_success_rate'] == 85.0
        assert metrics_dict['hallucination_rate'] == 5.0
        assert len(metrics_dict) == 15
    
    def test_metrics_average(self):
        metrics = MetricsScore(
            task_success_rate=100.0,
            pass_at_1=100.0,
            multi_file_edit_accuracy=100.0,
            planning_quality_score=100.0,
            tool_invocation_accuracy=100.0,
            context_retention=100.0,
            hallucination_rate=0.0,  # Will be inverted to 100
            scope_control=100.0,
            code_quality_score=100.0,
            security_awareness=100.0,
            recovery_rate=100.0,
            latency_per_step=1.0,  # Not included in average
            token_efficiency=1.0,  # Not included in average
            developer_intervention_rate=0.0,  # Will be inverted to 100
            output_stability=100.0,
        )
        
        avg = metrics.average()
        assert 90 <= avg <= 100  # High average
    
    def test_metrics_average_low_scores(self):
        metrics = MetricsScore(
            task_success_rate=20.0,
            pass_at_1=25.0,
            multi_file_edit_accuracy=30.0,
            planning_quality_score=25.0,
            tool_invocation_accuracy=20.0,
            context_retention=25.0,
            hallucination_rate=80.0,  # High hallucination
            scope_control=20.0,
            code_quality_score=25.0,
            security_awareness=20.0,
            recovery_rate=15.0,
            latency_per_step=10.0,
            token_efficiency=5000.0,
            developer_intervention_rate=80.0,
            output_stability=15.0,
        )
        
        avg = metrics.average()
        assert avg < 50  # Low average


class TestEvaluationResult:
    """Test evaluation result structure"""
    
    def test_result_to_dict(self):
        metrics = MetricsScore(
            task_success_rate=85.0,
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
        
        result = EvaluationResult(
            task_id="task_001",
            model_type=ModelType.GROQ,
            model_name="groq-model",
            task_description="Test problem",
            status=TaskStatus.SUCCESS,
            metrics=metrics,
            timestamp=datetime.now().isoformat(),
            execution_time=1.5,
        )
        
        result_dict = result.to_dict()
        assert result_dict['task_id'] == "task_001"
        assert result_dict['model_type'] == "groq"
        assert result_dict['status'] == "success"
        assert isinstance(result_dict['metrics'], dict)


class TestAgentEvaluator:
    """Test main evaluator"""
    
    def test_evaluator_initialization(self):
        evaluator = AgentEvaluator()
        assert len(evaluator.results) == 0
        assert len(evaluator.model_clients) == 0
    
    def test_register_model(self):
        evaluator = AgentEvaluator()
        mock_client = MockModelClient()
        
        evaluator.register_model(ModelType.GROQ, mock_client)
        
        assert ModelType.GROQ in evaluator.model_clients
        assert evaluator.model_clients[ModelType.GROQ] == mock_client
    
    def test_evaluate_task_missing_model(self):
        evaluator = AgentEvaluator()
        
        result = evaluator.evaluate_task(
            task_id="task_001",
            problem_statement="Test problem",
            language="python",
            model_type=ModelType.GROQ,
        )
        
        assert result.status == TaskStatus.ERROR
        assert "not registered" in result.error_message.lower()
    
    def test_evaluate_task_success(self):
        evaluator = AgentEvaluator()
        mock_client = MockModelClient()
        evaluator.register_model(ModelType.GROQ, mock_client)
        
        result = evaluator.evaluate_task(
            task_id="task_001",
            problem_statement="Test problem",
            language="python",
            model_type=ModelType.GROQ,
            num_test_runs=1,
        )
        
        assert result.status == TaskStatus.SUCCESS
        assert result.task_id == "task_001"
        assert result.model_name == "test-model"
        assert len(evaluator.results) == 1
    
    def test_compare_models(self):
        evaluator = AgentEvaluator()
        mock_client1 = MockModelClient("model1")
        mock_client2 = MockModelClient("model2")
        
        evaluator.register_model(ModelType.GROQ, mock_client1)
        evaluator.register_model(ModelType.OPENAI, mock_client2)
        
        # Evaluate with both models
        evaluator.evaluate_task(
            task_id="task_001",
            problem_statement="Test",
            language="python",
            model_type=ModelType.GROQ,
            num_test_runs=1,
        )
        
        comparison = evaluator.compare_models("task_001")
        
        assert "task_001" in comparison['task_id']
        assert "models" in comparison
    
    def test_get_summary_report_empty(self):
        evaluator = AgentEvaluator()
        summary = evaluator.get_summary_report()
        
        assert "error" in summary
    
    def test_get_summary_report_with_results(self):
        evaluator = AgentEvaluator()
        mock_client = MockModelClient()
        evaluator.register_model(ModelType.GROQ, mock_client)
        
        evaluator.evaluate_task(
            task_id="task_001",
            problem_statement="Test",
            language="python",
            model_type=ModelType.GROQ,
            num_test_runs=1,
        )
        
        summary = evaluator.get_summary_report()
        
        assert summary['total_evaluations'] == 1
        assert "models" in summary
        assert "test-model" in summary['models']
    
    def test_export_results_json(self, tmp_path):
        evaluator = AgentEvaluator()
        mock_client = MockModelClient()
        evaluator.register_model(ModelType.GROQ, mock_client)
        
        evaluator.evaluate_task(
            task_id="task_001",
            problem_statement="Test",
            language="python",
            model_type=ModelType.GROQ,
            num_test_runs=1,
        )
        
        filepath = tmp_path / "results.json"
        evaluator.export_results(str(filepath), format="json")
        
        with open(filepath) as f:
            data = json.load(f)
        
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]['task_id'] == "task_001"


class TestIntegration:
    """Integration tests"""
    
    def test_full_evaluation_pipeline(self):
        # Setup
        evaluator = AgentEvaluator()
        mock_client = MockModelClient("test-model-1")
        evaluator.register_model(ModelType.GROQ, mock_client)
        
        # Evaluate
        result = evaluator.evaluate_task(
            task_id="task_integration",
            problem_statement="Write a function to find maximum element",
            language="python",
            model_type=ModelType.GROQ,
            num_test_runs=2,
        )
        
        # Verify
        assert result.status == TaskStatus.SUCCESS
        assert result.metrics.task_success_rate >= 0
        assert result.metrics.task_success_rate <= 100
        
        # Summary
        summary = evaluator.get_summary_report()
        assert summary['total_evaluations'] == 1
        assert summary['models']['test-model-1']['num_tasks'] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
