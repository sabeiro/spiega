# Ollama + MCP gateway and Emacs assistant

This project runs **Ollama** (GPU) and an **MCP gateway** (tools + chat) in Docker behind **nginx**. **Open WebUI** is optional (commented out in `docker-compose.yml`). An **Emacs** config uses Ollama as an in-editor programming assistant via **gptel**.

**Architecture:** One LLM (Ollama). The MCP container is CPU-only (two processes: MCP protocol on 8000, FastAPI agent on 8001). nginx exposes it as a single endpoint: `/mcp` and `/mcp/*`; `/` and `/api/*` go to Ollama.

| Service   | Role |
|----------|------|
| **nginx** | HTTPS, reverse proxy; WebDAV share. |
| **ollama** | GPU; runs models (e.g. qwen2.5-coder, nemotron-3-nano). |
| **mcp**    | CPU; single endpoint `/mcp`: protocol (8000) + agent (8001: chat, control UI, tools); forwards LLM to ollama. |
| **pytorch** | Optional dev container (L4T PyTorch) for running scripts on the Jetson. |

---

## Emacs agentic assistant (gptel + Ollama)

The assistant uses **gptel** to talk to **Ollama** (e.g. **qwen2.5-coder:3b**) for code generation, explanations, and chat from inside Emacs.

### Prerequisites

1. **Ollama** running and reachable from the machine where you run Emacs:
   - If Emacs runs on the **same machine** as Ollama: Ollama must listen on `localhost:11434`.
   - If Emacs runs on **another machine** (e.g. your laptop): Ollama must be reachable at a host:port (e.g. `jetson:11434` or `192.168.x.x:11434`). The `emacs` config uses `jetson:11434` by default; change the `:host` in the Ollama backend if your hostname or port differ.

2. **Model** pulled in Ollama (on the machine that runs Ollama):
   ```bash
   ollama pull qwen2.5-coder:3b
   ```

3. **Emacs** with **MELPA** and the **gptel** package (the `emacs` config installs gptel automatically if missing).

### Config files

- **`emacs`** – Main init snippet (backends, keybindings, Minuet). It **loads** the gptel tools from `~/.emacs.d/gptel_tools.el`.
- **`gptel_tools.el`** – All gptel tool definitions (web, emacs, filesystem, system, ollama). **Copy this file to `~/.emacs.d/`** so the main config can load it. Customize **`gptel-system-commands-file`** and **`gptel-ollama-api-host`** there (or in your init after load).

### Changing the Ollama host

If Emacs runs on a different machine than Ollama, set the host in the `emacs` file. Find this block:

```elisp
(defvar gptel-jetson-backend
  (gptel-make-ollama "Jetson"
    :host "jetson:11434"   ; change to "localhost:11434" if Emacs and Ollama are on the same machine
    ...
```

- Remote Ollama: use your Jetson hostname or IP, e.g. `"jetson:11434"` or `"192.168.178.10:11434"`.

### Keybindings

| Key       | Action              |
|----------|---------------------|
| `C-c g`  | Open gptel (start a chat with the assistant) |
| `C-c C-g`| Send the current message / region to the assistant |

### Basic usage

1. Press **`C-c g`** to open a gptel buffer.
2. Type your question or select code in another buffer and send it (e.g. with **`C-c C-g`** when the gptel buffer is active, or as per gptel’s region/context behavior).
3. The assistant (default: **qwen2.5-coder:3b** via Ollama) replies in the same buffer.

You can ask for code snippets, explanations, refactors, or general programming help; the model is tuned for code.

### Switching backends

- **Jetson (default):** `M-x gptel-use-jetson` — uses Ollama on Jetson with **qwen2.5-coder:3b**. (`M-x gptel-use-ollama` is an alias.)
- **Azure OpenAI:** `M-x gptel-use-azure` — uses Azure; set `AZURE_OPENAI_KEY`, `AZURE_OPENAI_ENDPOINT`, and `AZURE_OPENAI_DEPLOYMENT` in your environment.

### Available Ollama models in this config

- **qwen2.5-coder:3b** (default) – programming assistant.
- **qwen2.5-coder:1.5b** – lighter/faster.
- **codellama**, **llama3.2**, **mistral** – also listed; pull with `ollama pull <name>` if you use them.

### Adding tools to gptel (Ollama agent)

gptel supports **tool use** (function calling): you define tools in Emacs, and when you send a prompt, gptel passes those tools to Ollama; the model can request tool calls, which gptel runs and feeds back. So the “agent” is gptel + Ollama together.

### How to use the tools (step by step)

**In Emacs (gptel):**

1. **Open gptel** – `C-c g` (or run `M-x gptel`).
2. **Choose which tools are active** – `M-x gptel-tools` to open the tools menu; enable or disable the tools you want for this chat (e.g. only filesystem, or only Ollama tools). By default all configured tools are on.
3. **Use a tool-capable model** – For the model to *call* tools, use one that supports tool use (e.g. **llama3.1**). Run `ollama pull llama3.1`, then in gptel choose model **llama3.1** (via the menu or set `gptel-model`). **qwen2.5-coder:3b** has limited tool support.
4. **Send a prompt** – Type what you want in natural language, e.g.:
   - *"List my Ollama models."*
   - *"Create a file hello.txt in /tmp with content 'Hello world'."*
   - *"Summarize the content of https://example.com."*
   - *"Append 'Done.' to the buffer named *scratch*."*
5. **Send** – `C-c C-g`. gptel sends your message and the tool list to Ollama. If the model decides to use a tool, gptel runs it and sends the result back; the model then continues and may call more tools or give a final answer. Responses with tools are non-streaming (they appear in one go).

**Ollama tools (included in this config):**

| Tool | What it does |
|------|----------------|
| **ollama_list_models** | Lists available Ollama model names on the configured host (e.g. jetson:11434). No arguments. |
| **ollama_generate** | Sends a prompt to Ollama and returns the generated text. Arguments: `prompt` (required), `model` (optional, default qwen2.5-coder:3b). Use for summarization, translation, or a quick answer from a specific model. |

The host for these Ollama tools is set by **`gptel-ollama-api-host`** in `gptel_tools.el` or your init (default `"jetson:11434"`). Set to `"localhost:11434"` if Emacs and Ollama run on the same machine.

**Other tools included (filesystem, Emacs, web):**

| Tool | What it does |
|------|----------------|
| **read_url** | Fetches a URL and returns the text content (needs libxml/shr). |
| **append_to_buffer** | Appends text to an Emacs buffer (creates it if needed). |
| **echo_message** | Writes a message to the *Messages* buffer. |
| **read_buffer** | Returns the full contents of an Emacs buffer by name. |
| **list_directory** | Lists entries in a directory. |
| **make_directory** | Creates a directory under a parent path. |
| **create_file** | Creates a file with given path, filename, and content. |
| **read_file** | Reads and returns the contents of a file (supports ~ and relative paths). |
| **run_shell_command** | Runs a bash command that **must exactly match** one line in an allowlist file. See below. |

You can say things like *"List files in /tmp"*, *"Create a file X with content Y"*, or *"What does https://... say?"* and the model can use these tools to do it.

**System commands (allowlist file):** gptel can run bash commands only if they are listed in an **allowlist file**. By default the file is **`gptel-allowed-commands.txt`** in the same directory as `gptel_tools.el` (i.e. `~/.emacs.d/gptel-allowed-commands.txt` when the tools file is in `.emacs.d`). Format: **one command per line**; lines starting with `#` and empty lines are ignored. Commands run from the **current buffer’s directory** (e.g. your project root). Set **`gptel-system-commands-file`** in `gptel_tools.el` or your init to use a different path. Example lines in the file:

```
date
pwd
ls -la
docker ps
```

The model can use **read_file** on that path to see what’s allowed, then call **run_shell_command** with exactly one of those lines (e.g. *"Run docker ps"* → `run_shell_command("docker ps")`). A sample **`gptel-allowed-commands.txt`** is included in this repo.

**1. Define tools**

Use `gptel-make-tool` (or `gptel-register-tool` if your gptel version uses it). Each tool has:

- **:name** – tool name the model will call
- **:description** – what the tool does (the model uses this to decide when to call it)
- **:args** – list of `(:name "arg" :type "string" :description "...")` for each parameter
- **:function** – Elisp function that receives the arguments and returns a string (result sent back to the model)
- **:category** – optional grouping (e.g. `"filesystem"`, `"search"`)

Example (create a file). The function receives one argument per `:args` entry, in order:

```elisp
(gptel-register-tool
 (gptel-make-tool
  :name "create_file"
  :description "Create a new file with the specified content."
  :args '((:name "path" :type string :description "Directory where to create the file")
          (:name "filename" :type string :description "Name of the file")
          (:name "content" :type string :description "Content to write"))
  :function (lambda (path filename content)
              (let ((full-path (expand-file-name filename path)))
                (with-temp-buffer
                  (insert content)
                  (write-region (point-min) (point-max) full-path))
                (format "Created file %s in %s" filename path)))
  :category "filesystem"))
```

**2. Select tools for a request**

- **`M-x gptel-tools`** – open the tools menu to enable/disable which tools are sent with the next request (e.g. buffer-local “scope”).
- Or set **`gptel-tools`** (buffer-local or global) to a list of tool names or tool objects you want available.

**3. Use a tool-capable model**

Ollama tool calling works best with models that support it (e.g. **llama3.1**, **qwen3**, **mistral**). **qwen2.5-coder:3b** may have limited or no tool support; for agent-style tool use, try e.g. `ollama pull llama3.1` and set `gptel-model` to `llama3.1` when using tools.

**4. Caveat**

With the Ollama backend, gptel **disables streaming** when tools are in use (tool use is non-streaming). So responses will appear in one go when tools are enabled.

**5. If you see “400 Bad Request” / “cannot unmarshal object into Go struct field ToolFunction.tools.function.name of type string”**

Ollama expects each tool’s `function.name` to be a JSON string. The **`gptel_tools.el`** in this repo adds an advice on `gptel--parse-tools` so that every tool name is sent as a string. Ensure you’re using this file (e.g. from `~/.emacs.d/`) and that parameter `:type` in tool args is the symbol `string` (not the string `"string"`). If the error persists, try a newer gptel and/or Ollama.

**References:** [gptel manual – Tool use](https://gptel.org/manual.html#Tool-use), [gptel issue #514 (tool use testing)](https://github.com/karthink/gptel/issues/514), [Ollama tool calling](https://docs.ollama.com/capabilities/tool-calling).

---

## Inline assistant (Minuet) – completion as you type

**Minuet** provides Copilot-style inline code completion using the same Ollama model (**qwen2.5-coder:3b**) via the FIM (fill-in-the-middle) API.

### How it is enabled

Inline completion is **manual by default**: press **`M-i`** in any buffer to request a suggestion. This avoids a known Minuet timer bug (`wrong-type-argument arrayp nil`) and avoids conflicts with python-mode when using `prog-mode-hook`.

- **Manual (default):** Use **`M-i`** whenever you want a suggestion. Works in Python and all other modes.
- **Automatic (optional):** In a buffer where you want as-you-type suggestions, run **`M-x minuet-auto-suggestion-mode`** once. You can add that to a specific mode hook in your config if you prefer (e.g. `python-mode-hook` only).

### Requirements

- **Emacs 29+** with native JSON (`(json-available-p)` should be non-nil).
- **Ollama** running with **qwen2.5-coder:3b** (same as gptel).
- Packages **minuet**, **plz**, and **dash** (the config installs them from MELPA if missing).

### If suggestions do not appear

1. Ensure Ollama is running and `ollama pull qwen2.5-coder:3b` has been run.
2. If Emacs runs on another machine than Ollama, change the Minuet endpoint in the `emacs` file: find `minuet-openai-fim-compatible-options` and set the `:end-point` to your Ollama URL, e.g. `"http://jetson:11434/v1/completions"` instead of `"http://localhost:11434/v1/completions"`.
3. Use **`M-i`** to request a suggestion manually; no auto-suggestion is enabled by default.

### Inline assistant keybindings

| Key    | Action |
|--------|--------|
| **`M-i`** | Request a suggestion (manual trigger). |
| **`M-y`** | Show completions in the minibuffer. |
| **`M-a`** | Accept one line of the suggestion (when visible). |
| **`M-A`** | Accept the whole suggestion. |
| **`Tab`** | Accept the first line (when a suggestion is visible). |
| **`M-e`** | Dismiss the suggestion. |
| **`M-n`** / **`M-p`** | Cycle to next/previous suggestion. |

---

## Adding tooling to your Ollama agent

You can give your agent **tools** (web search, code run, APIs, etc.) in two main ways.

### 1. Open WebUI (web interface)

Open WebUI supports **Tools**, **Functions**, and **Pipelines** that extend what the model can do.

- **Tools** – real-time data (weather, search, etc.). The model can call them during a chat.
- **Functions** – custom features, buttons, or model integrations (e.g. web search, home automation).
- **Pipelines** – multi-step workflows (RAG, heavy processing).

**How to add them:**

1. Open **https://webui.jetson** (or your Open WebUI URL) and log in.
2. Go to **Admin Panel** (gear icon) → **Plugins** / **Tools** / **Functions** (depending on version).
3. **From the community:** use [Open WebUI Community](https://openwebui.com/search) (or the in-UI “Explore” / “Get”): pick a plugin, paste your instance URL, review the code, then Save and enable.
4. **API keys:** if a plugin needs keys (e.g. web search), set them in the plugin’s settings (gear next to the plugin).
5. Enable the tool/function with its toggle and, if needed, attach it to a **Model** or **Agent** in **Connections** / **Agents**.

Docs: [Open WebUI Tools & Functions](https://docs.openwebui.com/features/plugin/), [Getting started with Functions](https://docs.openwebui.com/getting-started/quick-start/starting-with-functions/).

### 2. Ollama API (function calling)

For your own code (scripts, Emacs, other clients), Ollama’s API supports **tool calling**: you send a list of tools (name, description, parameters), and the model can return `tool_calls` that you execute and feed back.

- **Endpoint:** `POST http://<ollama-host>:11434/api/chat` (or the OpenAI-compatible `http://<ollama-host>:11434/v1`).
- **Request:** include a `tools` array (JSON schema per tool). The model replies with `message.tool_calls`; you run the tool, then send the result in a follow-up message.
- **Models:** many recent models support tools (e.g. Llama 3.1+, Qwen 3, Mistral Nemo). Your **qwen2.5-coder:3b** may have limited tool support; for strong tool use consider a model like **llama3.1** or **qwen3** and check [Ollama’s model list](https://ollama.com/library).

Docs: [Ollama – Tool calling](https://docs.ollama.com/capabilities/tool-calling).

**Summary:** Use **Open WebUI** for built-in and community tools in the web UI; use the **Ollama API** with `tools` when building your own agent (e.g. script or Emacs).

---

## Docker (Ollama + MCP + nginx)

- **Start:** `docker compose up -d` — runs nginx, ollama, mcp (gateway), and optionally the pytorch dev container.
- **Ollama** listens on `127.0.0.1:11434` (host); other containers use `http://ollama:11434` on the Docker network.
- **MCP** gateway: tools and `/api/chat`; connects to Ollama for the LLM. No GPU.
- **Nemotron 3 Nano** (optional): use Ollama instead of a separate vLLM stack — once the stack is up, run:
  ```bash
  docker exec -it ollama ollama pull nemotron-3-nano
  ```
  Then use the model like any other Ollama model (e.g. in MCP or gptel).
- **Open WebUI** is commented out in `docker-compose.yml`; uncomment and set `OLLAMA_BASE_URL=http://ollama:11434` if you want the web UI.
- **WebDAV** is served by nginx (see `default_nginx.conf`); storage is under `/srv/lav/` on the host (writable by www-data in the container).
- **Jetson / PyTorch:** see `install_dependencies.sh` and `JETSON_PYTORCH_DEPS.md` for host-side PyTorch + optional torchvision on JetPack 6.1.

The Emacs assistant (gptel) talks to Ollama directly (e.g. `localhost:11434` or `jetson:11434`), not through the MCP gateway.
