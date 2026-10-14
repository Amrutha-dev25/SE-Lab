Score progression: Pylint went 4.00, then 9.45, then 9.82, then 10.00. The last two steps came from the missing newline and then the mixed line endings.
Why you need all three tools: Pylint reached 10/10 while Bandit still reported security issues.
Overlap between tools: the bare except was caught by all three tools, eval by Pylint and Bandit, and unused variables by Pylint and Flake8.
Surprises: Notepad doesn’t add a final newline, and a PowerShell rewrite introduced mixed line endings that Pylint flagged.
Judgement calls: Bandit flags MD5 whatever it’s used for, but here the hash is an identifier. You still switched, and you can say SHA-256 alone doesn’t make a roll number hash safe.
Workflow: pre-commit hooks or CI that run all three tools before code is merged.

**What surprised me**

I learned that one unsafe coding practice can be detected by multiple static analysis tools. For example, removing `eval()` addressed both a code-quality warning from Pylint and a security warning from Bandit. I also learned that a high Pylint score alone does not guarantee that code is secure, which is why using all three tools is important.