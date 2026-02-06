# Synthesis Guide

This guide helps you combine outputs from the three Council agents into a cohesive "golden version" that balances creativity, accuracy, and robustness.

## Balance the Perspectives

Follow this sequence when synthesizing:

1. **Start with Accuracy's foundation** - Use the correctness and structure from the Accuracy Agent as the base
2. **Integrate Creativity's innovations** - Add modern patterns and elegant solutions where they don't compromise reliability
3. **Layer in Edge Cases' protections** - Add validation, error handling, and defensive checks comprehensively

## Resolve Conflicts

When agents disagree:

- **Creativity vs Accuracy**: Usually favor Accuracy unless the creative approach is clearly superior and still correct
- **Accuracy vs Edge Cases**: Integrate both - accuracy ensures it works, edge cases ensure it keeps working
- **Creativity vs Edge Cases**: Balance based on context - critical systems favor edge cases, user-facing tools can favor creativity
- **Performance vs Robustness**: Favor robustness unless performance is a stated requirement

## Avoid Pitfalls

- **Over-engineering**: Don't include every suggestion from every agent
- **Inconsistency**: Ensure the final code has a cohesive style
- **Redundancy**: Remove duplicate validations or error handling
- **Complexity**: Simplify where multiple agents overcomplicated

## The Golden Version Should

✅ Be correct and follow best practices (Accuracy)
✅ Use modern, elegant patterns where appropriate (Creativity)  
✅ Handle edge cases and errors comprehensively (Edge Cases)
✅ Be production-ready and maintainable
✅ Strike the right balance for the specific use case

## Context-Specific Adjustments

Different coding tasks warrant different balances. Adjust emphasis based on context:

### Prototypes & Demos
- **Balance**: Creativity (70%), Accuracy (20%), Edge Cases (10%)
- **Rationale**: Speed and elegance matter most, production robustness is secondary
- **Focus**: Make it work and make it impressive, worry about edge cases later

### Production Services
- **Balance**: Edge Cases (50%), Accuracy (35%), Creativity (15%)
- **Rationale**: Reliability and error handling are critical
- **Focus**: Must handle failures gracefully, uptime is paramount

### Libraries & APIs
- **Balance**: Accuracy (50%), Edge Cases (30%), Creativity (20%)
- **Rationale**: Correct, stable interfaces with good error handling
- **Focus**: Public contracts must be rock-solid and well-documented

### Internal Tools
- **Balance**: Creativity (40%), Accuracy (40%), Edge Cases (20%)
- **Rationale**: Balance usability with correctness
- **Focus**: Developer productivity matters, but tools must work reliably

### Algorithm Implementation
- **Balance**: Accuracy (60%), Edge Cases (30%), Creativity (10%)
- **Rationale**: Correctness of algorithm is paramount
- **Focus**: Get the algorithm right first, optimize later

### Data Processing Pipelines
- **Balance**: Accuracy (45%), Edge Cases (45%), Creativity (10%)
- **Rationale**: Must process data correctly and handle corrupt/missing data
- **Focus**: Correctness and resilience to bad data

### User Interfaces
- **Balance**: Creativity (50%), Accuracy (30%), Edge Cases (20%)
- **Rationale**: User experience and aesthetics drive adoption
- **Focus**: Make it delightful to use while being functionally correct

## Synthesis Process

1. **Read all three outputs** thoroughly
2. **Identify key differences** in approach, structure, and details
3. **Evaluate context** - What type of code is this? Who will use it? What are the consequences of failure?
4. **Choose the base** - Usually Accuracy Agent's structure provides the best foundation
5. **Integrate creative improvements** - Add modern patterns that enhance without compromising reliability
6. **Add defensive measures** - Layer in Edge Cases Agent's validations and error handling
7. **Remove redundancies** - Consolidate duplicate logic
8. **Ensure consistency** - Make sure the final code has a unified style and voice
9. **Validate completeness** - Does it solve the original task? Is anything missing?

## Red Flags

Watch for these issues when synthesizing:

❌ **Mixing incompatible paradigms** (e.g., functional + heavily stateful)
❌ **Validation overload** (checking the same thing 3 different ways)
❌ **Style inconsistency** (mixing verbose Accuracy style with minimal Creativity style)
❌ **Missing the task** (agents went in different directions, none fully solve it)
❌ **Over-abstraction** (too many layers trying to satisfy all agents)
❌ **Under-protection** (skipping important edge cases to preserve elegance)

## Example Synthesis

**Task**: Implement a function to parse CSV data

**Creativity Agent suggests**: 
- Fluent API design, generator pattern for memory efficiency
- Modern type hints with generics

**Accuracy Agent suggests**:
- Standard csv module usage, clear variable names
- Explicit error handling for file operations

**Edge Cases Agent suggests**:
- Validate file encoding, handle malformed CSV
- Empty file handling, memory limits for large files

**Golden Version synthesizes**:
```python
from typing import Generator, List
import csv

def parse_csv(filepath: str, max_rows: int = 1_000_000) -> Generator[List[str], None, None]:
    """Parse CSV file with memory-efficient streaming and robust error handling."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i >= max_rows:
                    raise ValueError(f"CSV exceeds maximum {max_rows} rows")
                yield row
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found: {filepath}")
    except csv.Error as e:
        raise ValueError(f"Malformed CSV at line {reader.line_num}: {e}")
```

**What was synthesized**:
- ✅ Creativity: Generator pattern, type hints, fluent design
- ✅ Accuracy: Standard library, clear names, proper exceptions  
- ✅ Edge Cases: Encoding handling, memory limits, error validation