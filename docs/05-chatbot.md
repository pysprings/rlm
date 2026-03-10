## Where it goes next: a chatbot

Look at the loop again. Messages arrive from two sources: the user (`"Query: ..."`) and the REPL (`"REPL output: ..."`). The model can't tell the difference — both are `"role": "user"`. We're already running a chatbot where the only participant is the REPL.

Adding a real human means: when the model stops writing code, instead of automatically looping with the same query, pause and wait for input.

~~~python
while True:
    resp = call_llm(msgs)
    if has_repl_blocks(resp):
        exec them, append outputs     # auto-continue
    else:
        display(resp)                  # show to user
        msgs.append(next_user_input()) # wait for human
~~~

The namespace persists across turns. If the model computed `summary = ...` in turn 1, the user can say "expand on that summary" in turn 3 and the model still has the variable. Like a Jupyter notebook that stays alive across a conversation.
