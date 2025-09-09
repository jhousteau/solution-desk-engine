# Analyze Agent Data

Analyze monitoring data from SOLVE agent phases, todo lists, and Claude telemetry for a specific issue.

## Arguments

Issue number to analyze (e.g., 156)

## System Prompt

You are analyzing agent performance data from SOLVE pipeline executions. Review monitoring data, todo completion, and telemetry to identify patterns and improvements. DO NOT create any files - just provide the analysis directly.

## User Prompt

Analyze agent performance data for issue #{{ISSUE_NUMBER}}:

1. **SOLVE Monitoring Data**:
   ```bash
   # Check for monitoring data for this specific issue
   MONITOR_DIR=".genesis/monitoring/solve-{{ISSUE_NUMBER}}"
   if [ -d "$MONITOR_DIR" ]; then
     echo "=== Monitoring Data Found for Issue {{ISSUE_NUMBER}} ==="
     ls -lh "$MONITOR_DIR"

     # Analyze interactions.jsonl
     if [ -f "$MONITOR_DIR/interactions.jsonl" ]; then
       echo ""
       echo "=== Interaction Log Analysis ==="
       echo "Total entries: $(wc -l < "$MONITOR_DIR/interactions.jsonl")"

       # Parse and analyze the JSONL data
       python3 -c "
import json
import sys
from datetime import datetime

phases = {}
errors = []
durations = []
prompt_sizes = []

with open('$MONITOR_DIR/interactions.jsonl', 'r') as f:
    for line in f:
        try:
            data = json.loads(line.strip())
            phase = data.get('phase', 'unknown')

            # Track phases
            if phase not in phases:
                phases[phase] = {'count': 0, 'success': 0, 'failed': 0}
            phases[phase]['count'] += 1

            # Track success/failure
            if data.get('success') == True:
                phases[phase]['success'] += 1
            elif data.get('success') == False:
                phases[phase]['failed'] += 1
                if 'error' in str(data.get('data', {})):
                    errors.append(data['data'].get('error', 'Unknown error'))

            # Track prompt sizes
            if 'prompt' in str(data.get('data', {})):
                prompt_data = data.get('data', {}).get('prompt', {})
                if isinstance(prompt_data, dict) and 'length' in prompt_data:
                    prompt_sizes.append(prompt_data['length'])

        except: pass

print('\\n=== Phase Summary ===')
for phase, stats in phases.items():
    if phase and phase != 'None':
        print(f'{phase}: {stats[\"count\"]} attempts, {stats[\"success\"]} success, {stats[\"failed\"]} failed')

if errors:
    print('\\n=== Errors Detected ===')
    for err in errors[:3]:  # Show first 3 errors
        print(f'- {err}')

if prompt_sizes:
    print(f'\\n=== Prompt Analysis ===')
    print(f'Average prompt size: {sum(prompt_sizes)/len(prompt_sizes):.0f} chars')
    print(f'Max prompt size: {max(prompt_sizes)} chars')
"
     fi

     # Check for analysis report if exists
     [ -f "$MONITOR_DIR/analysis-report.md" ] && echo -e "\n=== Previous Analysis Report Found ===" && head -20 "$MONITOR_DIR/analysis-report.md"
   else
     echo "No monitoring data found for issue {{ISSUE_NUMBER}}"
   fi
   ```

2. **Claude Telemetry Analysis**:
   ```bash
   # Search for issue-related telemetry in Claude logs
   echo -e "\n=== Claude Telemetry for Issue {{ISSUE_NUMBER}} ==="

   # Find relevant session logs
   TELEMETRY_FILES=$(find ~/.claude/projects -name "*.jsonl" -type f 2>/dev/null)

   if [ ! -z "$TELEMETRY_FILES" ]; then
     # Search for issue mentions in telemetry
     for file in $TELEMETRY_FILES; do
       ISSUE_MENTIONS=$(grep -c "{{ISSUE_NUMBER}}" "$file" 2>/dev/null || echo "0")
       if [ "$ISSUE_MENTIONS" -gt 0 ]; then
         echo "Found $ISSUE_MENTIONS mentions in $(basename $(dirname $file))/$(basename $file)"

         # Extract relevant telemetry
         grep "{{ISSUE_NUMBER}}" "$file" | python3 -c "
import json, sys
tool_uses = 0
todo_updates = 0
timestamps = []

for line in sys.stdin:
    try:
        data = json.loads(line)
        if 'toolUse' in str(data):
            tool_uses += 1
        if 'TodoWrite' in str(data):
            todo_updates += 1
        if 'timestamp' in data:
            timestamps.append(data['timestamp'])
    except: pass

if timestamps:
    print(f'  Time range: {timestamps[0]} to {timestamps[-1]}')
print(f'  Tool uses: {tool_uses}')
print(f'  Todo updates: {todo_updates}')
" 2>/dev/null
       fi
     done
   fi

   # Check todo persistence for this issue
   TODO_FILES=$(find ~/.claude/todos -name "*-agent-*.json" -size +10c 2>/dev/null | head -5)
   if [ ! -z "$TODO_FILES" ]; then
     echo -e "\n=== Todo List State ==="
     for file in $TODO_FILES; do
       if grep -q "{{ISSUE_NUMBER}}" "$file" 2>/dev/null; then
         echo "Todo file with issue {{ISSUE_NUMBER}}: $(basename $file)"
         python3 -c "
import json
with open('$file', 'r') as f:
    todos = json.load(f)
    completed = sum(1 for t in todos if t.get('status') == 'completed')
    in_progress = sum(1 for t in todos if t.get('status') == 'in_progress')
    pending = sum(1 for t in todos if t.get('status') == 'pending')
    print(f'  Completed: {completed}, In Progress: {in_progress}, Pending: {pending}')
    print(f'  Total: {len(todos)}, Completion: {completed}/{len(todos)} ({100*completed/len(todos):.1f}%)')
"
       fi
     done
   fi
   ```

3. **Phase-Specific Analysis**:
   ```bash
   # Check if scaffold.md was created
   [ -f worktrees/solve-{{ISSUE_NUMBER}}/.solve/scaffold.md ] && echo "Scaffold: ✅ Created" || echo "Scaffold: ❌ Not created"
   [ -f worktrees/solve-{{ISSUE_NUMBER}}/.solve/outline.md ] && echo "Outline: ✅ Created" || echo "Outline: ❌ Not created"
   [ -f worktrees/solve-{{ISSUE_NUMBER}}/.solve/logic.md ] && echo "Logic: ✅ Created" || echo "Logic: ❌ Not created"
   [ -f worktrees/solve-{{ISSUE_NUMBER}}/.solve/verify.md ] && echo "Verify: ✅ Created" || echo "Verify: ❌ Not created"
   [ -f worktrees/solve-{{ISSUE_NUMBER}}/.solve/enhance.md ] && echo "Enhance: ✅ Created" || echo "Enhance: ❌ Not created"

   # Check GitHub comments
   echo "=== GitHub Comments ==="
   gh issue view {{ISSUE_NUMBER}} --json comments --jq '.comments | length' | xargs -I {} echo "Total comments: {}"
   ```

4. **Generate Analysis Summary**:
   Based on the data above, provide:
   - **Pipeline Status**: Success/Failed and at which phase
   - **Failure Analysis**: Root cause if failed
   - **Performance Metrics**: Time taken, output compliance
   - **Todo Completion Rate**: X/Y tasks completed
   - **Key Issues Identified**: Bullet points of problems
   - **Recommendations**: Specific actionable improvements

   Format as a concise report without creating any files.

## Context

SOLVE framework phase constraints:
- **Scaffold**: 10 min, 50 lines max
- **Outline**: 15 min, 100 lines max
- **Logic**: 20 min, 150 lines max
- **Verify**: 15 min, 100 lines max
- **Enhance**: 5 min, 50 lines max

## Instructions

Provide a concise analysis focusing on:
1. What phase failed and why
2. Specific metrics (time, output size, todo completion)
3. Actionable recommendations
4. No file creation - just the analysis output
