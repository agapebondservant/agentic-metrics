## RULE: Optional Use of OpenRewrite for Java Codebases
1. IF this is a Java codebase and a relevant OpenRewrite recipe exists for a task, it should be prioritized over manual coding.
2. IF no OpenRewrite recipe exists for a task, fall back to AI-driven implementation.

## RULE: Adaptive Security Gate
STRICT REQUIREMENT: Every "Apply" phase MUST include a security scan.
1. **PICK TOOL:** Use the best available tool (e.g., `pmd`, `eslint`, or `grep`).
2. **SCAN:** Check all new/modified code for secrets, evals, or injections.
3. **LOG:** You MUST write "Security Check: [Tool Name] - PASSED" in the apply summary.
4. **BLOCK:** If any High/Critical risks are found, STOP and fix them first.