# Basic OpenAI Agent Demo

This folder contains the smallest possible demo showing how to:

* Build an **agent** that uses OpenAI's function-calling interface ("tools").
* Wrap it in a **Chainlit** chat UI so users can interact in the browser.
* Expose a single, very simple tool – it just returns the current date & time.

---

## 1. Prerequisites

1. **Activate your main virtual environment** (the one that lives in your project root):

```bash
$ source ../venv/bin/activate  # adapt the path if needed
```

2. Install the (small) Python dependencies once:

```bash
(venv) $ pip install -r requirements.txt
```

3. Provide your OpenAI credentials. Either export it in the shell:

```bash
(venv) $ export OPENAI_API_KEY="sk-your-key"
```

or duplicate the sample env file:

```bash
(venv) $ cp .env.example .env  # then edit the file and paste your key
```

---

## 2. Running the agent

```bash
(venv) $ chainlit run agent_app.py -w  # -w enables hot-reload
```

Open the URL printed by Chainlit (usually http://localhost:8000) and start chatting!

Try asking something like:

> What time is it right now?

The model will decide to call the local `get_current_datetime` tool and reply with the result.

---

## 3. File overview

* `agent_app.py` – The entire app (≈100 lines). Defines the tool and handles the OpenAI calls.
* `requirements.txt` – Minimal dependency list.
* `.env.example` – Template for your OpenAI API key + optional model override.

That's it – enjoy experimenting! 🎉 