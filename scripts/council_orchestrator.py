#!/usr/bin/env python3
"""
Council of 3 Orchestrator
Spawns 3 parallel coding agents with different focuses and synthesizes their outputs.
"""

import json
import sys
from typing import Dict, List
import asyncio
import aiohttp


AGENT_PROMPTS = {
    "creativity": """You are the CREATIVITY AGENT in a council of 3 coding agents.

Your focus: Innovation, novel approaches, and creative solutions.
- Prioritize elegant, innovative designs
- Explore unconventional approaches
- Consider modern patterns and emerging best practices
- Think about developer experience and code aesthetics
- Don't be afraid to suggest cutting-edge solutions

Complete the coding task with creativity as your primary lens.""",
    
    "accuracy": """You are the ACCURACY AGENT in a council of 3 coding agents.

Your focus: Correctness, precision, and following established best practices.
- Prioritize correctness and reliability above all
- Follow language idioms and conventions strictly
- Ensure type safety and proper error handling
- Use well-tested, proven approaches
- Focus on maintainability and clarity

Complete the coding task with accuracy as your primary lens.""",
    
    "edge_cases": """You are the EDGE CASES AGENT in a council of 3 coding agents.

Your focus: Robustness, error handling, and covering unusual scenarios.
- Prioritize defensive programming
- Consider boundary conditions, null/empty inputs, race conditions
- Think about error states and failure modes
- Add comprehensive input validation
- Consider security implications and edge cases
- Plan for scalability and performance issues

Complete the coding task with edge case handling as your primary lens."""
}


async def call_claude_api(session: aiohttp.ClientSession, prompt: str, task: str) -> Dict:
    """Call Claude API with the given system prompt and task."""
    url = "https://api.anthropic.com/v1/messages"
    
    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 4000,
        "system": prompt,
        "messages": [
            {"role": "user", "content": task}
        ]
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    async with session.post(url, json=payload, headers=headers) as response:
        return await response.json()


async def spawn_council(task: str) -> Dict[str, str]:
    """Spawn 3 agents in parallel to complete the task."""
    async with aiohttp.ClientSession() as session:
        tasks_list = [
            call_claude_api(session, AGENT_PROMPTS["creativity"], task),
            call_claude_api(session, AGENT_PROMPTS["accuracy"], task),
            call_claude_api(session, AGENT_PROMPTS["edge_cases"], task)
        ]
        
        results = await asyncio.gather(*tasks_list)
        
        # Extract text responses
        outputs = {}
        agent_names = ["creativity", "accuracy", "edge_cases"]
        
        for i, (agent_name, result) in enumerate(zip(agent_names, results)):
            if "content" in result:
                text_content = ""
                for block in result["content"]:
                    if block.get("type") == "text":
                        text_content += block.get("text", "")
                outputs[agent_name] = text_content
            else:
                outputs[agent_name] = f"Error: {result.get('error', {}).get('message', 'Unknown error')}"
        
        return outputs


def format_council_results(outputs: Dict[str, str]) -> str:
    """Format the council outputs for the synthesizer."""
    formatted = "# Council of 3 Agent Outputs\n\n"
    
    formatted += "## Creativity Agent Output\n"
    formatted += "Focus: Innovation, novel approaches, creative solutions\n\n"
    formatted += outputs["creativity"] + "\n\n"
    formatted += "---\n\n"
    
    formatted += "## Accuracy Agent Output\n"
    formatted += "Focus: Correctness, precision, best practices\n\n"
    formatted += outputs["accuracy"] + "\n\n"
    formatted += "---\n\n"
    
    formatted += "## Edge Cases Agent Output\n"
    formatted += "Focus: Robustness, error handling, edge cases\n\n"
    formatted += outputs["edge_cases"] + "\n\n"
    
    return formatted


async def main():
    if len(sys.argv) < 2:
        print("Usage: python council_orchestrator.py '<coding task>'")
        sys.exit(1)
    
    task = sys.argv[1]
    
    print("🏛️  Convening the Council of 3...")
    print(f"📋 Task: {task}\n")
    
    # Spawn the 3 agents in parallel
    print("🤖 Spawning agents:")
    print("   • Creativity Agent (innovative solutions)")
    print("   • Accuracy Agent (correctness & best practices)")
    print("   • Edge Cases Agent (robustness & error handling)\n")
    
    outputs = await spawn_council(task)
    
    print("✅ All agents have completed their work\n")
    
    # Format results for synthesis
    formatted_outputs = format_council_results(outputs)
    
    # Output the results as JSON for Claude to parse
    print(json.dumps({
        "status": "success",
        "outputs": outputs,
        "formatted": formatted_outputs
    }))


if __name__ == "__main__":
    asyncio.run(main())