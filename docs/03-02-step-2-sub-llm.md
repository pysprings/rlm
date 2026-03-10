## Step 2: Give the LLM a sub-LLM

The killer feature isn't just "LLM writes Python." It's that the Python can call *another LLM*. We inject a function into the namespace:

~~~python
ns["llm_query"] = lambda prompt: call_openai(prompt)
~~~

Now the model can write:

~~~python
chunk = context[:10000]
summary = llm_query(f"Summarize this: {chunk}")
print(summary)
~~~

This is where "recursive" comes from. The LLM writes code that calls an LLM. In the full version, that inner LLM could itself be an RLM — turtles all the way down. We keep it at one level.
