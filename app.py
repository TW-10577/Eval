"""
Streamlit web interface for AI Code Evaluator
"""

import streamlit as st
import json
import pandas as pd
from datetime import datetime

from evaluator import AgentEvaluator, ModelType
from model_clients import GroqModelClient, OpenAIModelClient, LlamaLocalClient


# Configure Streamlit
st.set_page_config(
    page_title="AI Code Evaluator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .score-high { color: #09ab3b; font-weight: bold; }
    .score-medium { color: #ff8c00; font-weight: bold; }
    .score-low { color: #d62728; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'evaluator' not in st.session_state:
        st.session_state.evaluator = AgentEvaluator()
    if 'results' not in st.session_state:
        st.session_state.results = []
    if 'comparison_data' not in st.session_state:
        st.session_state.comparison_data = {}


def register_models():
    """Register available models"""
    models_available = {}
    
    try:
        groq_client = GroqModelClient()
        st.session_state.evaluator.register_model(ModelType.GROQ, groq_client)
        models_available['Groq (Cloud)'] = ModelType.GROQ
    except Exception as e:
        st.warning(f"⚠️ Groq not available: {str(e)[:100]}")
    
    try:
        openai_client = OpenAIModelClient()
        st.session_state.evaluator.register_model(ModelType.OPENAI, openai_client)
        models_available['OpenAI GPT-4 (Cloud)'] = ModelType.OPENAI
    except Exception as e:
        st.warning(f"⚠️ OpenAI not available: {str(e)[:100]}")
    
    try:
        llama_client = LlamaLocalClient(model_name="llama2")
        st.session_state.evaluator.register_model(ModelType.LLAMA_LOCAL, llama_client)
        models_available['Llama 2 (Local)'] = ModelType.LLAMA_LOCAL
    except Exception as e:
        st.warning(f"⚠️ Llama not available: {str(e)[:100]}")
    
    return models_available


def render_score(score: float, max_val: float = 100) -> str:
    """Render score with color coding"""
    percentage = (score / max_val) * 100 if max_val > 0 else 0
    
    if percentage >= 80:
        color_class = "score-high"
    elif percentage >= 60:
        color_class = "score-medium"
    else:
        color_class = "score-low"
    
    return f'<span class="{color_class}">{score:.1f}</span>'


def main():
    # Initialize
    initialize_session_state()
    
    # Header
    st.title("🤖 AI Coding Agent Evaluator")
    st.markdown("Evaluate and compare LLM coding assistants across 15 core metrics")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Register models
        models_available = register_models()
        
        if not models_available:
            st.error("❌ No models available. Please configure API keys or Ollama.")
            return
        
        st.success(f"✅ {len(models_available)} model(s) available")
        
        # Model selection
        selected_model = st.selectbox(
            "Select Model to Test:",
            options=list(models_available.keys()),
            help="Choose one model to evaluate at a time"
        )
        
        # Task configuration
        st.subheader("📋 Task Configuration")
        
        task_mode = st.radio(
            "Task Input Mode:",
            options=["Predefined Examples", "Custom Problem"]
        )
        
        if task_mode == "Predefined Examples":
            predefined_tasks = {
                "Palindrome Substring": "Find the longest palindromic substring in a string",
                "Fibonacci": "Calculate fibonacci number at position n with memoization",
                "Graph BFS": "Implement BFS algorithm for graph traversal",
                "Sort Array": "Sort an array in ascending order without using built-in sort",
                "Tree Traversal": "Implement in-order, pre-order, and post-order traversal"
            }
            task_name = st.selectbox("Choose a task:", list(predefined_tasks.keys()))
            problem_statement = predefined_tasks[task_name]
        else:
            problem_statement = st.text_area(
                "Enter problem statement:",
                height=150,
                placeholder="Describe your coding problem here..."
            )
            task_name = "Custom Task"
        
        programming_language = st.selectbox(
            "Programming Language:",
            options=["python", "javascript", "java", "cpp", "golang"]
        )
        
        num_test_runs = st.slider(
            "Number of test runs (for stability):",
            min_value=1,
            max_value=5,
            value=2
        )
        
        # Evaluation button
        if st.button("🚀 Run Evaluation", use_container_width=True):
            if not problem_statement:
                st.error("Please enter a problem statement")
                return
            
            if not selected_model:
                st.error("Please select a model")
                return
            
            with st.spinner("⏳ Evaluating model... This may take a few minutes..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                model_type = models_available[selected_model]
                status_text.text(f"Evaluating {selected_model}...")
                
                result = st.session_state.evaluator.evaluate_task(
                    task_id=task_name,
                    problem_statement=problem_statement,
                    language=programming_language,
                    model_type=model_type,
                    num_test_runs=num_test_runs
                )
                
                st.session_state.results.append(result)
                progress_bar.progress(1.0)
                
                status_text.text("✅ Evaluation complete!")
                st.balloons()
    
    # Main content tabs
    if st.session_state.results:
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Results",
            "📈 All Model Results",
            "📋 Detailed Metrics",
            "💾 Export"
        ])
        
        with tab1:
            st.subheader("Evaluation Results")
            
            for result in st.session_state.results:
                with st.container():
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.write(f"### {result.model_name}")
                    
                    with col2:
                        score = result.metrics.average()
                        st.metric(
                            "Overall Score",
                            f"{score:.1f}",
                            delta=f"out of 100"
                        )
                    
                    with col3:
                        st.metric(
                            "Status",
                            result.status.value.upper()
                        )
                    
                    # Key metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric(
                            "Task Success",
                            f"{result.metrics.task_success_rate:.1f}%"
                        )
                    
                    with col2:
                        st.metric(
                            "Pass@1",
                            f"{result.metrics.pass_at_1:.1f}%"
                        )
                    
                    with col3:
                        st.metric(
                            "Code Quality",
                            f"{result.metrics.code_quality_score:.1f}"
                        )
                    
                    with col4:
                        st.metric(
                            "Hallucination",
                            f"{result.metrics.hallucination_rate:.1f}%",
                            delta="should be low"
                        )
                    
                    st.divider()
        
        with tab2:
            st.subheader("All Model Results")
            
            # Prepare results data
            results_data = {
                "Model": [],
                "Overall Score": [],
                "Task Success": [],
                "Pass@1": [],
                "Code Quality": [],
                "Context Retention": [],
                "Hallucination Rate": [],
                "Test Time": []
            }
            
            for result in st.session_state.results:
                results_data["Model"].append(result.model_name)
                results_data["Overall Score"].append(result.metrics.average())
                results_data["Task Success"].append(result.metrics.task_success_rate)
                results_data["Pass@1"].append(result.metrics.pass_at_1)
                results_data["Code Quality"].append(result.metrics.code_quality_score)
                results_data["Context Retention"].append(result.metrics.context_retention)
                results_data["Hallucination Rate"].append(result.metrics.hallucination_rate)
                results_data["Test Time"].append(result.timestamp)
            
            df = pd.DataFrame(results_data)
            
            # Display table
            st.dataframe(df, use_container_width=True)
            
            # Charts
            if len(df) > 1:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.bar_chart(df.set_index("Model")[["Overall Score", "Code Quality"]])
                
                with col2:
                    st.bar_chart(df.set_index("Model")[["Task Success", "Pass@1"]])
            else:
                st.info("Run evaluations for multiple models to see comparison charts")
        
        with tab3:
            st.subheader("Detailed Metrics (15 Core Parameters)")
            
            for result in st.session_state.results:
                with st.expander(f"📌 {result.model_name}", expanded=False):
                    metrics = result.metrics
                    
                    # Create metrics table
                    metrics_data = {
                        "Metric": [
                            "1. Task Success Rate",
                            "2. Pass@1 (Functional Correctness)",
                            "3. Multi-File Edit Accuracy",
                            "4. Planning Quality Score",
                            "5. Tool Invocation Accuracy",
                            "6. Context Retention",
                            "7. Hallucination Rate",
                            "8. Scope Control",
                            "9. Code Quality Score",
                            "10. Security Awareness",
                            "11. Recovery/Self-Correction",
                            "12. Latency per Step (s)",
                            "13. Token Efficiency",
                            "14. Developer Intervention Rate",
                            "15. Output Stability",
                        ],
                        "Score": [
                            metrics.task_success_rate,
                            metrics.pass_at_1,
                            metrics.multi_file_edit_accuracy,
                            metrics.planning_quality_score,
                            metrics.tool_invocation_accuracy,
                            metrics.context_retention,
                            metrics.hallucination_rate,
                            metrics.scope_control,
                            metrics.code_quality_score,
                            metrics.security_awareness,
                            metrics.recovery_rate,
                            metrics.latency_per_step,
                            metrics.token_efficiency,
                            metrics.developer_intervention_rate,
                            metrics.output_stability,
                        ]
                    }
                    
                    df_metrics = pd.DataFrame(metrics_data)
                    st.dataframe(df_metrics, use_container_width=True)
        
        with tab4:
            st.subheader("Export Results")
            
            # JSON export
            json_data = [r.to_dict() for r in st.session_state.results]
            json_str = json.dumps(json_data, indent=2)
            
            st.download_button(
                label="📥 Download as JSON",
                data=json_str,
                file_name=f"evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
            
            # CSV export
            comparison_data = {
                "Model": [],
                "Overall Score": [],
                "Task Success": [],
                "Pass@1": [],
                "Code Quality": [],
                "Context Retention": [],
                "Hallucination Rate": [],
                "Timestamp": []
            }
            
            for result in st.session_state.results:
                comparison_data["Model"].append(result.model_name)
                comparison_data["Overall Score"].append(result.metrics.average())
                comparison_data["Task Success"].append(result.metrics.task_success_rate)
                comparison_data["Pass@1"].append(result.metrics.pass_at_1)
                comparison_data["Code Quality"].append(result.metrics.code_quality_score)
                comparison_data["Context Retention"].append(result.metrics.context_retention)
                comparison_data["Hallucination Rate"].append(result.metrics.hallucination_rate)
                comparison_data["Timestamp"].append(result.timestamp)
            
            df_export = pd.DataFrame(comparison_data)
            csv = df_export.to_csv(index=False)
            
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    else:
        # Welcome message
        st.info("""
        ## 👋 Welcome to AI Code Evaluator
        
        **How to use:**
        1. Configure your models in the sidebar
        2. Choose or write a coding problem
        3. Select one model to test
        4. Click "Run Evaluation"
        5. Repeat with different models to test them individually
        
        ### 📊 15 Core Metrics
        - Task Success Rate
        - Pass@1 (Functional Correctness)
        - Multi-File Edit Accuracy
        - Planning Quality Score
        - Tool Invocation Accuracy
        - Context Retention
        - Hallucination Rate
        - Scope Control
        - Code Quality Score
        - Security Awareness
        - Recovery/Self-Correction Rate
        - Latency per Step
        - Token Efficiency
        - Developer Intervention Rate
        - Output Stability
        """)


if __name__ == "__main__":
    main()
