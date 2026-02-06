---
name: co3
description: Multi-agent coding approach that spawns 3 parallel AI agents with different focuses (creativity, accuracy, edge cases) to solve coding tasks, then synthesizes their outputs into a golden version. Use for coding tasks, algorithm design, code planning, architecture decisions, debugging complex issues, code reviews, or any coding task that benefits from multiple perspectives. Triggers include requests like co3, use council of 3, get multiple perspectives, or when user explicitly requests this multi-agent approach for coding.
---

# Council of 3

## Overview

The Council of 3 approach spawns three parallel AI agents, each with a specialized focus, to complete the same coding task independently. After all three agents finish, the main Claude synthesizes their outputs into a single "golden version" that combines the best aspects of all three perspectives.

## The Three Agents

Each agent approaches the task through a different lens:

1. **Creativity Agent**: Focuses on innovation, novel approaches, elegant designs, and modern patterns
2. **Accuracy Agent**: Focuses on correctness, reliability, established best practices, and maintainability  
3. **Edge Cases Agent**: Focuses on robustness, error handling, boundary conditions, and defensive programming

**For detailed agent behavior guidelines**, see:
- `references/creativity-agent.md` - Philosophy, priorities, and behavioral guidelines for the Creativity Agent
- `references/accuracy-agent.md` - Philosophy, priorities, and behavioral guidelines for the Accuracy Agent
- `references/edge-cases-agent.md` - Philosophy, priorities, and behavioral guidelines for the Edge Cases Agent
- `references/synthesis-guide.md` - How to effectively combine outputs and resolve conflicts

## Workflow

Follow this workflow when the user requests the Council of 3 approach:

### Step 1: Clarify the Task

Ensure the coding task is well-defined. If ambiguous, ask clarifying questions before proceeding:
- What is the specific coding task?
- Are there any constraints or requirements?
- What programming language(s)?
- Any specific libraries or frameworks to use/avoid?

### Step 2: Spawn the Three Agents in Parallel

Use the bash_tool to spawn three parallel agents via the Anthropic API. The API authentication is handled automatically in this environment.

Create three temporary files with the specialized prompts:

```bash
# Creativity Agent Prompt
cat > /tmp/creativity_prompt.txt << 'EOF'
You are the CREATIVITY AGENT in a council of 3 coding agents.

Your focus: Innovation, novel approaches, and creative solutions.
- Prioritize elegant, innovative designs
- Explore unconventional approaches
- Consider modern patterns and emerging best practices
- Think about developer experience and code aesthetics
- Don't be afraid to suggest cutting-edge solutions

Complete the coding task with creativity as your primary lens.
EOF

# Accuracy Agent Prompt
cat > /tmp/accuracy_prompt.txt << 'EOF'
You are the ACCURACY AGENT in a council of 3 coding agents.

Your focus: Correctness, precision, and following established best practices.
- Prioritize correctness and reliability above all
- Follow language idioms and conventions strictly
- Ensure type safety and proper error handling
- Use well-tested, proven approaches
- Focus on maintainability and clarity

Complete the coding task with accuracy as your primary lens.
EOF

# Edge Cases Agent Prompt
cat > /tmp/edge_cases_prompt.txt << 'EOF'
You are the EDGE CASES AGENT in a council of 3 coding agents.

Your focus: Robustness, error handling, and covering unusual scenarios.
- Prioritize defensive programming
- Consider boundary conditions, null/empty inputs, race conditions
- Think about error states and failure modes
- Add comprehensive input validation
- Consider security implications and edge cases
- Plan for scalability and performance issues

Complete the coding task with edge case handling as your primary lens.
EOF
```

Then spawn the three agents in parallel using curl:

```bash
# Launch all three agents in parallel
for agent in creativity accuracy edge_cases; do
  (
    curl -X POST https://api.anthropic.com/v1/messages \
      -H "Content-Type: application/json" \
      -d "{
        \"model\": \"claude-sonnet-4-20250514\",
        \"max_tokens\": 4000,
        \"system\": \"$(cat /tmp/${agent}_prompt.txt)\",
        \"messages\": [{\"role\": \"user\", \"content\": \"$TASK\"}]
      }" > /tmp/${agent}_output.json
  ) &
done

# Wait for all agents to complete
wait
```

### Step 3: Parse Agent Outputs

Extract the text content from each agent's response:

```bash
# Extract text from each agent
for agent in creativity accuracy edge_cases; do
  jq -r '.content[] | select(.type=="text") | .text' /tmp/${agent}_output.json > /tmp/${agent}.txt
done
```

### Step 4: Synthesize the Golden Version

**Before synthesizing, read:**
- `references/synthesis-guide.md` - Comprehensive synthesis strategies, conflict resolution, and context-specific balancing
- Individual agent files as needed to understand their specific approaches

Review all three agent outputs (stored in `/tmp/creativity.txt`, `/tmp/accuracy.txt`, `/tmp/edge_cases.txt`) and create a synthesized solution that:

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

**User request:** "co3 design a file upload handler with validation"

Or: "Use council of 3 to design a file upload handler with validation"

**Process:**
1. Spawn three agents with task: "Design a file upload handler with validation in Python"
2. Creativity Agent might suggest: async processing, elegant class design, modern type hints
3. Accuracy Agent might suggest: proper file I/O, standard validation patterns, clear error messages
4. Edge Cases Agent might suggest: file size limits, MIME type validation, malicious file detection
5. Synthesize: Combine async design + proper validation + comprehensive security checks

## Resources

### references/creativity-agent.md

Detailed guide for the Creativity Agent:
- Philosophy: Innovation and elegance over convention
- Core priorities and behavioral guidelines
- Example tendencies and when to emphasize this agent

### references/accuracy-agent.md

Detailed guide for the Accuracy Agent:
- Philosophy: Correctness above all
- Core priorities and behavioral guidelines  
- Example tendencies and when to emphasize this agent

### references/edge-cases-agent.md

Detailed guide for the Edge Cases Agent:
- Philosophy: Murphy's law - plan for everything that can go wrong
- Core priorities and behavioral guidelines
- Example tendencies and when to emphasize this agent

### references/synthesis-guide.md

Comprehensive guide for combining agent outputs into a golden version:
- How to balance the three perspectives
- Conflict resolution strategies
- Context-specific adjustments (prototypes vs production vs libraries)
- Common pitfalls to avoid
- Example synthesis walkthrough

**Read the synthesis guide before combining outputs** to understand how to create an effective golden version.

## Implementation Notes

The Council of 3 approach works by spawning three parallel Claude instances via the Anthropic API. Authentication is handled automatically in this environment, so no API keys need to be configured. The agents run in parallel for efficiency, each receiving the same task but with different system prompts that shape their focus.

**Requirements:**
- `curl` for API calls (typically pre-installed)
- `jq` for JSON parsing (install with `apt-get install jq` if needed)
