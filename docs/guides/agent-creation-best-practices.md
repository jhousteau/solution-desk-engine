# Agent Creation Best Practices for Claude Code

This document provides comprehensive best practices for creating optimized agents (subagents) in Claude Code based on Anthropic's recommendations and Claude Code's subagent framework.

## Core Principles

### 1. Single Responsibility Design
- **Create focused agents** with one clear, specific purpose
- Avoid trying to make one agent handle everything
- Better to have multiple specialized agents than one generalized agent
- Each agent should have a distinct expertise area

### 2. Clear Proactive Triggering
- Use action-oriented descriptions that specify when the agent should be used
- Include trigger words like "PROACTIVELY", "MUST BE USED", or "Use immediately"
- Make descriptions specific to the task context, not generic
- Test descriptions to ensure Claude Code delegates appropriately

### 3. Minimal Tool Access
- Grant only tools that are essential for the agent's specific purpose
- Use explicit tool lists rather than inheriting all tools when possible
- Consider security implications of tool access
- Review tool permissions regularly

### 4. Detailed System Prompts
- Write comprehensive system prompts with specific instructions
- Include examples of expected behavior and outputs
- Define constraints and limitations clearly
- Specify output formats and quality criteria

## Agent Architecture Best Practices

### Naming Conventions
```yaml
# Good Examples
name: business-analyst
name: solution-architect-gcp
name: domain-expert-franchise

# Avoid
name: general-helper
name: do_everything_agent
name: BusinessAnalyst (use hyphens, not camelCase)
```

### Description Field Optimization

**Effective Description Pattern:**
```yaml
description: "[Role] specialist for [Phase/Task]. Use PROACTIVELY when [specific conditions]. Triggers: [specific scenarios]."
```

**Examples:**
```yaml
# Good - Specific and actionable
description: "Document analysis specialist for Phase 0. Use PROACTIVELY when cataloging source materials, creating inventories, or mapping document dependencies."

# Poor - Too generic
description: "Helps with business analysis tasks"
```

### Tool Selection Strategy

**Option 1: Explicit Tool List (Recommended)**
```yaml
tools: Read, Write, Grep, Glob  # Specific tools only
```

**Option 2: Inherit All Tools**
```yaml
# Omit tools field entirely - inherits all available tools
```

**Tool Selection Guidelines:**
- **Read, Write**: Document creation and analysis
- **Grep, Glob**: Code and file searching
- **Bash**: Command execution (use cautiously)
- **WebSearch, WebFetch**: External research
- **MCP tools**: Domain-specific capabilities

## Prompt Engineering for Agents

### Role Definition Framework

Use this template for effective role definition:

```markdown
You are a [specific title] with [X years] of experience in [domain].
You specialize in [specific expertise areas].

Your primary responsibilities:
1. [Specific task 1]
2. [Specific task 2]
3. [Specific task 3]

Your approach:
- [Methodology step 1]
- [Methodology step 2]
- [Methodology step 3]
```

### Task Decomposition Patterns

**Standard Task Flow:**
```markdown
When invoked:
1. [Analysis phase]
2. [Planning phase]
3. [Execution phase]
4. [Validation phase]
5. [Documentation phase]
```

**Example:**
```markdown
When invoked:
1. Analyze source documents for key information
2. Identify relationships and dependencies
3. Create structured inventory
4. Validate completeness and accuracy
5. Document findings with clear recommendations
```

### Success Criteria Specification

Define clear, measurable success criteria:

```markdown
Success Criteria:
- [ ] All source documents cataloged
- [ ] Key relationships mapped
- [ ] Dependencies identified
- [ ] Gaps documented
- [ ] Next phase requirements defined
```

### Error Handling Instructions

```markdown
Error Handling:
- If document is unreadable, note format issue and continue
- If information is missing, explicitly document gaps
- If conflicts exist, present options with recommendations
- Always provide partial results rather than failing completely
```

### Output Format Requirements

```markdown
Output Format:
- Executive summary (2-3 sentences)
- Detailed findings (structured list)
- Key insights (bullet points)
- Recommendations (actionable items)
- Next steps (specific actions)
```

## Advanced Agent Patterns

### Chaining Agents Strategy

Design agents to work together effectively:

```yaml
# Phase 0 Agent
name: document-analyzer
description: "Phase 0 source analysis specialist. Use PROACTIVELY for document cataloging. Hands off to research agents for Phase 1."

# Phase 1 Agent
name: problem-researcher
description: "Phase 1 problem analysis specialist. Use PROACTIVELY after Phase 0 completion for problem statement research."
```

### Context Preservation Techniques

```markdown
Context Management:
- Start with brief summary of previous phase outputs
- Reference specific source documents by name
- Maintain consistent terminology across agents
- Document assumptions and constraints clearly
```

### Proactive Triggering Patterns

**Time-based Triggers:**
- "Use immediately after [event]"
- "Use PROACTIVELY when Phase X is complete"

**Condition-based Triggers:**
- "Use when document analysis is needed"
- "Use PROACTIVELY for technical architecture tasks"

**Content-based Triggers:**
- "Use when working with franchise/lease content"
- "Use for Google Cloud related technical decisions"

## Performance Optimization

### Context Window Management

```markdown
Context Efficiency Tips:
- Reference previous work without repeating content
- Use structured formats to minimize token usage
- Focus on incremental additions to knowledge
- Summarize rather than duplicate information
```

### Tool Usage Optimization

```markdown
Tool Usage Best Practices:
- Use Read for specific document analysis
- Use Grep for targeted content searching
- Use Write for structured output creation
- Avoid unnecessary Bash commands
- Batch file operations when possible
```

### Memory and State Management

```markdown
State Management:
- Agents start fresh each invocation
- Document all context in outputs
- Create clear handoff documentation
- Maintain consistent data formats
```

## Testing and Validation

### Agent Behavior Testing

```markdown
Test Scenarios:
1. Correct invocation (should trigger when expected)
2. Tool usage (uses only necessary tools)
3. Output format (matches specifications)
4. Error handling (graceful failure modes)
5. Integration (works with other agents)
```

### Description Trigger Testing

```markdown
Trigger Test Matrix:
- Test with relevant task descriptions ✓
- Test with similar but different tasks ✗
- Test with generic requests ✗
- Test with explicit agent mentions ✓
```

### Quality Validation Checklist

```markdown
Agent Quality Gates:
- [ ] Single, clear responsibility
- [ ] Proactive trigger words included
- [ ] Tool access minimized appropriately
- [ ] System prompt is comprehensive
- [ ] Output format is specified
- [ ] Error handling is defined
- [ ] Success criteria are measurable
- [ ] Integration points are clear
```

## Common Anti-Patterns to Avoid

### 1. Swiss Army Knife Agents
```yaml
# AVOID - Too broad
description: "General business helper for any task"

# BETTER - Specific focus
description: "Document inventory specialist for Phase 0 source analysis"
```

### 2. Unclear Triggering
```yaml
# AVOID - Vague conditions
description: "Helps with technical stuff"

# BETTER - Specific triggers
description: "Google Cloud architecture specialist. Use PROACTIVELY for technical solution design."
```

### 3. Tool Over-Permissioning
```yaml
# AVOID - Unnecessary tools
tools: Read, Write, Bash, WebSearch, Edit, MultiEdit, NotebookEdit, WebFetch

# BETTER - Minimal necessary tools
tools: Read, Write, mcp__Ref__ref_search_documentation
```

### 4. Generic System Prompts
```markdown
<!-- AVOID -->
You are a helpful assistant that does business analysis.

<!-- BETTER -->
You are a Senior Business Analyst with 15+ years of experience in document
analysis and requirements gathering. You specialize in creating comprehensive
source inventories and mapping complex document relationships.
```

## Agent Lifecycle Management

### Development Workflow
1. **Define Purpose**: Single, specific responsibility
2. **Design Triggers**: Clear proactive conditions
3. **Select Tools**: Minimal necessary access
4. **Write Prompt**: Detailed system instructions
5. **Test Behavior**: Validate triggering and output
6. **Iterate**: Refine based on performance
7. **Document**: Update best practices

### Version Control Best Practices
```bash
# Store project agents in version control
.claude/agents/
├── business-analyst.md
├── domain-expert-franchise.md
└── solution-architect-gcp.md

# Create user agents for personal use
~/.claude/agents/
└── personal-productivity-agent.md
```

### Team Collaboration
```markdown
Team Agent Guidelines:
- Use descriptive commit messages for agent changes
- Document agent purpose in team documentation
- Share successful agent patterns
- Maintain consistent naming conventions
- Review agent performance regularly
```

## Success Metrics

### Agent Effectiveness Measures
- **Trigger Accuracy**: How often Claude Code correctly delegates tasks
- **Output Quality**: Consistency and usefulness of agent outputs
- **Tool Efficiency**: Appropriate tool usage without over-permissioning
- **Integration Success**: How well agents work together in workflows
- **Time Savings**: Reduction in manual work through agent automation

### Continuous Improvement Process
1. Monitor agent usage patterns
2. Collect feedback on agent outputs
3. Identify common failure modes
4. Refine descriptions and prompts
5. Update tool permissions as needed
6. Share learnings with team

---

## Templates and Examples

See the `agents/` subdirectory for complete agent persona examples:
- [Business Analyst Agent](agents/business-analyst-agent.md)
- [Domain Expert Agent](agents/domain-expert-agent.md)
- [Solution Architect Agent](agents/solution-architect-agent.md)

These examples demonstrate the application of these best practices for specific use cases in the solution development methodology.
