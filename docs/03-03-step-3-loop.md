## Step 3: The conversation loop

The LLM doesn't solve everything in one shot. It iterates: look at the data, write some code, see the output, think, write more code. We model this as a multi-turn chat where REPL outputs show up as messages:

~~~text
 System:     You have a REPL with `context` and `llm_query`.

 User:       Query: What's the main argument?

 Assistant:  Let me look at the structure first.
             ~~~repl
             print(context[:500])
             ~~~

 User:       REPL output:
             Chapter 1: Introduction to Pottery...

 Assistant:  Interesting, it's about pottery. Let me chunk and summarize.
             ~~~repl
             chunks = [context[i:i+10000] for i in range(0, len(context), 10000)]
             results = [llm_query(f"Summarize: {c}") for c in chunks]
             print(results)
             ~~~

 User:       REPL output:
             ['Chapter 1 discusses...', 'Chapter 2 argues...', ...]

 Assistant:  ~~~repl
             answer = llm_query(f"Combine: {results}")
             FINAL(answer)
             ~~~
~~~

Notice the rhythm. The model writes code in `` ```repl `` blocks. We extract those blocks, run them, and feed the output back as the next "user" message. The model never sees the raw document in its context window — only the slices it asks for.

Here's the loop as code. This is the heart of the whole thing — everything else is setup around it:

~~~python
for _ in range(max_iters):
    msgs.append({"role": "user", "content": f"Query: {query}"})

    resp = call_llm(msgs)
    msgs.append({"role": "assistant", "content": resp})

    for code in find_repl_blocks(resp):
        output = run_in_namespace(code, ns)
        msgs.append({"role": "user", "content": f"REPL output:\n{output}"})
~~~

Three appends per iteration: the prompt, the response, and each REPL result. That's the whole conversation protocol.
