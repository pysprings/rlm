## Step 6: Putting it together

Here's the complete namespace — four injected names that define the model's entire API surface:

~~~python
ns = {
    "context": context,               # the data to explore
    "FINAL":   final,                  # signal "I have my answer"
    "print":   our_capture_lambda,     # see intermediate results
    "llm_query": our_openai_wrapper,   # call a sub-LLM
}
~~~

And here's the complete loop:

~~~python
for _ in range(max_iters):
    msgs.append({"role": "user", "content": f"Query: {query}"})
    resp = client.chat.completions.create(model=model, messages=msgs)
    msgs.append({"role": "assistant", "content": resp})

    for code in re.findall(r'```repl\s*\n(.*?)\n```', resp, re.DOTALL):
        output.clear()
        try:
            exec(code, ns)
        except _Done as d:
            return d.value
        except Exception as e:
            output.append(f"Error: {e}")
        out = "\n".join(output) or "(no output)"
        msgs.append({"role": "user", "content": f"REPL output:\n{out}"})

return resp  # ran out of iterations
~~~

That's the whole algorithm. One regex, one exec, one exception class, one loop, one namespace dict.
