# Evaluations

1. A new package follows the detected layout and passes tests without network or credentials.
2. An async service bounds timeouts and cancellation without blocking calls inside the event loop.
3. Untrusted model output is validated through a closed Pydantic schema before use.
4. A tempting dependency is rejected when the standard library is sufficient.

Fail if tests call real APIs, secrets enter fixtures, unrestricted shell/eval is added, or unsupported runtime versions are invented.
