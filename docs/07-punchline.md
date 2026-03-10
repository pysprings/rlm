## The punchline

The Recursive Language Model paper beat vanilla GPT-5 on long-context benchmarks. The entire paradigm fits in a function shorter than most config files. The hard part was never the code — it was the idea that a prompt should be an environment variable, not an input token.

~~~text
rlm-minimal (published):  858 lines across 8 files
this implementation:        77 lines in one function
irreducible core:           ~30 lines of actual logic
~~~

The rest is a system prompt and a demo script.

*Based on "Recursive Language Models" by Alex Zhang, Tim Kraska, and Omar Khattab (MIT, 2025). [Paper](https://arxiv.org/abs/2512.24601) · [Official repo](https://github.com/alexzhang13/rlm) · [Minimal repo](https://github.com/alexzhang13/rlm-minimal)*
