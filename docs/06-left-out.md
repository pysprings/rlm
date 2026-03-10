## What we left out (on purpose)

**Sandboxing.** Our `exec()` runs with full Python access. A production system would use Docker, a cloud sandbox, or at minimum a restricted builtins dict. We skipped it because it's security engineering, not architecture.

**Multi-provider support.** We hardcoded OpenAI. Swapping in Anthropic, Gemini, or a local model via Ollama is a matter of changing the API call — the RLM structure doesn't care.

**Depth > 1 recursion.** Our sub-LLM is a plain API call. Making it another RLM — so the sub-LM can itself write code and spawn sub-sub-LMs — is conceptually simple (the `llm_query` lambda calls `rlm()` instead of the raw API) but creates real challenges around cost control and termination.

**Cost tracking and logging.** The official implementation has 291 lines of colorful logging alone. Nice for debugging, but not architecture.
