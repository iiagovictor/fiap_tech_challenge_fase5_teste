"""
ReAct (Reasoning + Acting) agent for financial analysis.

Implements the ReAct pattern:
1. Thought: Reason about what to do next
2. Action: Execute a tool or search for information
3. Observation: Observe the result
4. Repeat until answer is found

Uses LiteLLM for cloud-agnostic LLM access.
"""

import json
import logging
import re
from typing import Any

from litellm import completion

from src.agent.rag_pipeline import get_rag_pipeline
from src.agent.tools import TOOLS
from src.config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class ReactAgent:
    """
    ReAct agent for answering financial questions with tools and RAG.
    
    Follows the ReAct pattern: Thought -> Action -> Observation -> Answer
    """

    def __init__(self):
        self.rag = get_rag_pipeline()
        self.tools = {tool["name"]: tool["function"] for tool in TOOLS}
        self.max_iterations = 5

    def _build_system_prompt(self) -> str:
        """Build system prompt with tool descriptions."""
        tool_descriptions = []
        for tool in TOOLS:
            params = ", ".join([f"{k}: {v['type']}" for k, v in tool["parameters"].items()])
            tool_descriptions.append(
                f"- {tool['name']}({params}): {tool['description']}"
            )

        tools_text = "\n".join(tool_descriptions)

        return f"""You are a financial analysis assistant with access to stock market data and analysis tools.

You follow the ReAct (Reasoning + Acting) pattern:
1. Thought: Think about what you need to do
2. Action: Use a tool or search knowledge base
3. Observation: Analyze the result
4. Repeat until you have enough information
5. Answer: Provide the final answer

Available Tools:
{tools_text}

Format your responses as:
Thought: [your reasoning]
Action: [tool_name(param1="value1", param2="value2")]
Observation: [result from tool]
... (repeat as needed)
Answer: [final answer to the user]

When you have enough information, provide a clear, concise answer.
"""

    def _call_llm(self, messages: list[dict]) -> str:
        """Call LLM via LiteLLM."""
        try:
            response = completion(
                model=settings.llm_model,
                messages=messages,
                temperature=settings.llm_temperature,
                max_tokens=settings.llm_max_tokens,
                api_base=settings.llm_base_url if "ollama" in settings.llm_model else None,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return f"Error: {str(e)}"

    def _parse_action(self, text: str) -> tuple[str | None, dict]:
        """
        Parse action from agent output.
        
        Expected format: Action: tool_name(param1="value1", param2="value2")
        """
        action_pattern = r"Action:\s*(\w+)\((.*?)\)"
        match = re.search(action_pattern, text, re.IGNORECASE)

        if not match:
            return None, {}

        tool_name = match.group(1)
        params_str = match.group(2)

        # Parse parameters
        params = {}
        if params_str:
            # Simple parameter parsing (handles strings and lists)
            param_pattern = r'(\w+)=(["\'])(.*?)\2'
            for param_match in re.finditer(param_pattern, params_str):
                param_name = param_match.group(1)
                param_value = param_match.group(3)
                params[param_name] = param_value

        return tool_name, params

    def _execute_tool(self, tool_name: str, params: dict) -> Any:
        """Execute a tool with given parameters."""
        if tool_name not in self.tools:
            return f"Error: Tool '{tool_name}' not found"

        try:
            tool_func = self.tools[tool_name]
            result = tool_func(**params)
            return result
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            return f"Error: {str(e)}"

    def query(self, user_query: str) -> dict:
        """
        Process a user query using the ReAct pattern.
        
        Args:
            user_query: User's question
        
        Returns:
            Dictionary with answer, reasoning steps, and tool calls
        """
        logger.info(f"Processing query: {user_query}")

        # Retrieve relevant context from RAG
        context = self.rag.retrieve_context(user_query, n_results=2)

        # Build messages
        system_prompt = self._build_system_prompt()
        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Context from knowledge base:\n{context}\n\nUser Question: {user_query}",
            },
        ]

        reasoning_steps = []
        tool_calls = []

        for iteration in range(self.max_iterations):
            logger.info(f"Iteration {iteration + 1}/{self.max_iterations}")

            # Get LLM response
            response = self._call_llm(messages)
            reasoning_steps.append(response)

            # Check if answer is provided
            if "Answer:" in response:
                # Extract final answer
                answer = response.split("Answer:")[-1].strip()
                logger.info("✅ Agent provided final answer")

                return {
                    "query": user_query,
                    "answer": answer,
                    "reasoning_steps": reasoning_steps,
                    "tool_calls": tool_calls,
                    "iterations": iteration + 1,
                }

            # Parse and execute action
            tool_name, params = self._parse_action(response)

            if tool_name:
                logger.info(f"Executing tool: {tool_name} with params {params}")
                tool_result = self._execute_tool(tool_name, params)
                tool_calls.append({"tool": tool_name, "params": params, "result": tool_result})

                # Add observation to messages
                observation = f"Observation: {json.dumps(tool_result, indent=2)}"
                messages.append({"role": "assistant", "content": response})
                messages.append({"role": "user", "content": observation})
            else:
                # No action found, ask LLM to continue
                messages.append({"role": "assistant", "content": response})
                messages.append(
                    {
                        "role": "user",
                        "content": "Please continue with your analysis or provide the final answer.",
                    }
                )

        # Max iterations reached
        logger.warning("Max iterations reached without final answer")
        return {
            "query": user_query,
            "answer": "I apologize, but I wasn't able to complete the analysis within the allowed steps. Please try rephrasing your question.",
            "reasoning_steps": reasoning_steps,
            "tool_calls": tool_calls,
            "iterations": self.max_iterations,
            "error": "max_iterations_reached",
        }


def get_agent() -> ReactAgent:
    """Get ReAct agent instance."""
    return ReactAgent()


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Test agent (requires Ollama running locally)
    agent = get_agent()

    # Test query
    print("\n🤖 Testing ReAct Agent\n")
    query = "What is the current technical analysis for ITUB4.SA?"

    print(f"Query: {query}\n")
    result = agent.query(query)

    print(f"\nAnswer: {result['answer']}")
    print(f"\nTool Calls: {len(result['tool_calls'])}")
    print(f"Iterations: {result['iterations']}")
