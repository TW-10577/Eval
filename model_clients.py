"""
Model clients for different LLM backends
Implements: Groq, OpenAI, and Local Llama via Ollama
"""

import os
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
import json

from evaluator import ModelClient
from langchain_ollama import OllamaLLM

load_dotenv()


class GroqModelClient(ModelClient):
    """Client for Groq cloud LLM"""
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "mixtral-8x7b-32768"):
        super().__init__("groq", model_name)
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Groq client"""
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment. Set it in .env file or pass api_key parameter.")
        try:
            from groq import Groq
            self.client = Groq(api_key=self.api_key)
        except ImportError:
            raise ImportError("groq library not installed. Run: pip install groq")
        except Exception as e:
            raise ValueError(f"Failed to initialize Groq client: {str(e)}")
    
    def generate_test_cases(self, problem: str, language: str, num_cases: int = 5) -> List[Dict]:
        """Generate test cases using Groq"""
        prompt = f"""Generate {num_cases} test cases for this {language} problem:

Problem: {problem}

Return a JSON array with objects containing:
- input: the test input
- expected_output: expected output
- description: what this test case validates

Format: [{{...}}, {{...}}]"""
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
                temperature=0.5,
                max_tokens=2000,
            )
            
            content = response.choices[0].message.content
            # Extract JSON from response
            start = content.find('[')
            end = content.rfind(']') + 1
            json_str = content[start:end]
            test_cases = json.loads(json_str)
            return test_cases
        except Exception as e:
            print(f"Error generating test cases with Groq: {e}")
            return []
    
    def evaluate_code(self, code: str, problem: str, language: str) -> Dict[str, Any]:
        """Evaluate code quality using Groq"""
        prompt = f"""Evaluate this {language} code for a problem:

Problem: {problem}

Code:
```{language}
{code}
```

Rate these aspects (0-100):
- Correctness: Does it solve the problem?
- Efficiency: Time and space complexity
- Readability: Code clarity and organization
- Robustness: Error handling and edge cases
- Maintainability: Code structure and documentation

Return JSON with scores for each."""
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
                temperature=0.5,
                max_tokens=1000,
            )
            
            content = response.choices[0].message.content
            start = content.find('{')
            end = content.rfind('}') + 1
            json_str = content[start:end]
            evaluation = json.loads(json_str)
            return evaluation
        except Exception as e:
            print(f"Error evaluating code with Groq: {e}")
            return {}
    
    def analyze_planning(self, problem: str) -> Dict[str, Any]:
        """Analyze task decomposition quality"""
        prompt = f"""For this coding problem, analyze the planning approach:

Problem: {problem}

Provide a JSON with:
- steps: list of key steps to solve this
- complexity: estimated problem difficulty (1-10)
- edge_cases: important edge cases to consider
- planning_score: quality of decomposition (0-100)"""
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
                temperature=0.5,
                max_tokens=1000,
            )
            
            content = response.choices[0].message.content
            start = content.find('{')
            end = content.rfind('}') + 1
            json_str = content[start:end]
            planning = json.loads(json_str)
            return planning
        except Exception as e:
            print(f"Error analyzing planning with Groq: {e}")
            return {}


class OpenAIModelClient(ModelClient):
    """Client for OpenAI GPT models"""
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gpt-4"):
        super().__init__("openai", model_name)
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize OpenAI client"""
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment. Set it in .env file or pass api_key parameter.")
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("openai library not installed. Run: pip install openai")
        except Exception as e:
            raise ValueError(f"Failed to initialize OpenAI client: {str(e)}")
    
    def generate_test_cases(self, problem: str, language: str, num_cases: int = 5) -> List[Dict]:
        """Generate test cases using OpenAI"""
        prompt = f"""Generate {num_cases} test cases for this {language} problem:

Problem: {problem}

Return a JSON array with objects containing:
- input: the test input
- expected_output: expected output
- description: what this test case validates

Format: [{{...}}, {{...}}]"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=2000,
            )
            
            content = response.choices[0].message.content
            start = content.find('[')
            end = content.rfind(']') + 1
            json_str = content[start:end]
            test_cases = json.loads(json_str)
            return test_cases
        except Exception as e:
            print(f"Error generating test cases with OpenAI: {e}")
            return []
    
    def evaluate_code(self, code: str, problem: str, language: str) -> Dict[str, Any]:
        """Evaluate code quality using OpenAI"""
        prompt = f"""Evaluate this {language} code for a problem:

Problem: {problem}

Code:
```{language}
{code}
```

Rate these aspects (0-100):
- Correctness: Does it solve the problem?
- Efficiency: Time and space complexity
- Readability: Code clarity and organization
- Robustness: Error handling and edge cases
- Maintainability: Code structure and documentation

Return JSON with scores for each."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=1000,
            )
            
            content = response.choices[0].message.content
            start = content.find('{')
            end = content.rfind('}') + 1
            json_str = content[start:end]
            evaluation = json.loads(json_str)
            return evaluation
        except Exception as e:
            print(f"Error evaluating code with OpenAI: {e}")
            return {}
    
    def analyze_planning(self, problem: str) -> Dict[str, Any]:
        """Analyze task decomposition quality"""
        prompt = f"""For this coding problem, analyze the planning approach:

Problem: {problem}

Provide a JSON with:
- steps: list of key steps to solve this
- complexity: estimated problem difficulty (1-10)
- edge_cases: important edge cases to consider
- planning_score: quality of decomposition (0-100)"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=1000,
            )
            
            content = response.choices[0].message.content
            start = content.find('{')
            end = content.rfind('}') + 1
            json_str = content[start:end]
            planning = json.loads(json_str)
            return planning
        except Exception as e:
            print(f"Error analyzing planning with OpenAI: {e}")
            return {}


class LlamaLocalClient(ModelClient):
    """Client for local Llama via Ollama"""
    
    def __init__(self, model_name: str = "llama2", base_url: str = "http://localhost:11434"):
        super().__init__("llama", model_name)
        self.base_url = base_url
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Ollama client"""
        try:
            self.client = OllamaLLM(model=self.model_name, base_url=self.base_url)
        except ImportError:
            raise ImportError("langchain-ollama library not installed. Run: pip install langchain-ollama")
        except Exception as e:
            raise ValueError(f"Failed to connect to Ollama at {self.base_url}. Make sure Ollama is running: ollama serve. Error: {str(e)}")
    # ...existing code...
    
    def generate_test_cases(self, problem: str, language: str, num_cases: int = 5) -> List[Dict]:
        """Generate test cases using local Llama"""
        prompt = f"""Generate {num_cases} test cases for this {language} problem:

Problem: {problem}

Return a JSON array with objects containing:
- input: the test input
- expected_output: expected output
- description: what this test case validates

Respond with ONLY valid JSON, starting with [ and ending with ]"""
        
        try:
            response = self.client.invoke(prompt)
            # Extract JSON from response
            start = response.find('[')
            end = response.rfind(']') + 1
            json_str = response[start:end]
            test_cases = json.loads(json_str)
            return test_cases
        except Exception as e:
            print(f"Error generating test cases with Llama: {e}")
            return []
    
    def evaluate_code(self, code: str, problem: str, language: str) -> Dict[str, Any]:
        """Evaluate code quality using local Llama"""
        prompt = f"""Evaluate this {language} code for a problem:

Problem: {problem}

Code:
```{language}
{code}
```

Rate these aspects (0-100):
- Correctness: Does it solve the problem?
- Efficiency: Time and space complexity
- Readability: Code clarity and organization
- Robustness: Error handling and edge cases
- Maintainability: Code structure and documentation

Respond with ONLY valid JSON."""
        
        try:
            response = self.client.invoke(prompt)
            start = response.find('{')
            end = response.rfind('}') + 1
            json_str = response[start:end]
            evaluation = json.loads(json_str)
            return evaluation
        except Exception as e:
            print(f"Error evaluating code with Llama: {e}")
            return {}
    
    def analyze_planning(self, problem: str) -> Dict[str, Any]:
        """Analyze task decomposition quality"""
        prompt = f"""For this coding problem, analyze the planning approach:

Problem: {problem}

Provide a JSON with:
- steps: list of key steps to solve this
- complexity: estimated problem difficulty (1-10)
- edge_cases: important edge cases to consider
- planning_score: quality of decomposition (0-100)

Respond with ONLY valid JSON."""
        
        try:
            response = self.client.invoke(prompt)
            start = response.find('{')
            end = response.rfind('}') + 1
            json_str = response[start:end]
            planning = json.loads(json_str)
            return planning
        except Exception as e:
            print(f"Error analyzing planning with Llama: {e}")
            return {}
