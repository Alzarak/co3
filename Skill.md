---
name: council-of-3
description: Multi-agent coding approach that spawns 3 parallel AI agents with different focuses (creativity, accuracy, edge cases) to solve coding tasks, then synthesizes their outputs into a golden version. Use for coding tasks, algorithm design, code planning, architecture decisions, debugging complex issues, code reviews, or any coding task that benefits from multiple perspectives. Triggers include requests like use council of 3 or get multiple perspectives or when user explicitly requests this multi-agent approach for coding.
---

# Council of 3

## Overview

The Council of 3 approach spawns three parallel AI agents, each with a specialized focus, to complete the same coding task independently. After all three agents finish, the main Claude synthesizes their outputs into a single "golden version" that combines the best aspects of all three perspectives.

## The Three Agents

Each agent approaches the task through a different lens:

1. **Creativity Agent**: Focuses on innovation, novel approaches, elegant designs, and modern patterns
2. **Accuracy Agent**: Focuses on correctness, reliability, established best practices, and maintainability  
3. **Edge Cases Agent**: Focuses on robustness, error handling, boundary conditions, and defensive programming

## Workflow

Follow this workflow when the user requests the Council of 3 approach:

### Step 1: Clarify the Task

Ensure the coding task is well-defined. If ambiguous, ask clarifying questions before proceeding:
- What is the specific coding task?
- Are there any constraints or requirements?
- What programming language(s)?
- Any specific libraries or frameworks to use/avoid?

### Step 2: Run the Council Orchestrator

Execute the council orchestrator script with the task:

```bash
python /path/to/scripts/council_orchestrator.py "Your coding task here"
```

The script will:
- Spawn 3 agents in parallel via the Anthropic API
- Each agent receives the same task with its specialized system prompt
- Wait for all agents to complete
- Return formatted outputs from all three agents

### Step 3: Parse Agent Outputs

The script returns JSON with three outputs:
```json
{
  "status": "success",
  "outputs": {
    "creativity": "...",
    "accuracy": "...", 
    "edge_cases": "..."
  },
  "formatted": "Markdown-formatted version of all outputs"
}
```

### Step 4: Synthesize the Golden Version

Review all three agent outputs and create a synthesized solution that:

- **Incorporates creative insights** from the Creativity Agent where they enhance the solution
- **Ensures correctness** by validating against the Accuracy Agent's approach
- **Adds robustness** by including edge case handling from the Edge Cases Agent
- **Balances trade-offs** between elegance, correctness, and defensive programming
- **Produces production-ready code** that combines the best of all three perspectives

When synthesizing:
- Start with the Accuracy Agent's foundation (ensures correctness)
- Integrate creative approaches that don't sacrifice reliability
- Add edge case handling and error checking comprehensively
- Remove redundancies where agents overlapped
- Ensure the final code is cohesive and well-structured

### Step 5: Present the Golden Version

Present only the final synthesized version to the user. Do not show the three individual agent outputs unless the user specifically asks to see them.

Include:
- The synthesized code
- Brief explanation of how you combined the three perspectives
- Key insights from each agent that were incorporated

## Best Practices

- **Use for complex tasks**: The Council approach adds latency, so reserve it for tasks that truly benefit from multiple perspectives
- **Clear task definition**: Vague tasks lead to divergent agent outputs that are hard to synthesize
- **Trust the process**: Each agent's "extreme" focus is intentional - synthesis balances them
- **Handle API errors**: If any agent fails, inform the user and offer to retry or continue with available outputs

## Example Usage

**User request:** "Use council of 3 to design a file upload handler with validation"

**Process:**
1. Run orchestrator with task: "Design a file upload handler with validation in Python"
2. Creativity Agent might suggest: async processing, elegant class design, modern type hints
3. Accuracy Agent might suggest: proper file I/O, standard validation patterns, clear error messages
4. Edge Cases Agent might suggest: file size limits, MIME type validation, malicious file detection
5. Synthesize: Combine async design + proper validation + comprehensive security checks

## Resources

### scripts/council_orchestrator.py

The main orchestrator script that manages the three-agent workflow. It uses the Anthropic API to spawn agents in parallel with specialized system prompts and returns their combined outputs for synthesis.