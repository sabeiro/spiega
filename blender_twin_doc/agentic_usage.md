# Agentic Usage Guide for Emacs + MCP Servers

This guide documents how to use Emacs with Model Context Protocol (MCP) servers, GPTel, Aider, Llama (Ollama), and Pi-coding workflows to create an intelligent, tool-augmented development environment.

---

## Overview

This setup transforms Emacs from a simple editor into an **agentic project coordinator** that can:

- Call LLM APIs (Ollama, custom models)
- Use MCP servers to access tools (filesystem, git, Blender, ROS, etc.)
- Run code directly in buffers
- Generate and apply patches
- Coordinate multiple tools (git, Blender-ROS, Ollama, etc.)

The core packages we enable:

| Package | Purpose |
|---------|-------------|
| **GPTel** | LLM client with tool integration |
| **MCP-Hub** | Centralised MCP client |
| **Aider** | AI code editing tool |
| **Ollama** | Local LLM server |
| **Pi-coding** | Personal AI coding assistant |

---

## Useful Commands

### 1. **GPTel Commands**

```elisp
M-x gptel-load-and-call       ;; Load and run GPTel
M-x gptel-send                ;; Send prompt to backend
M-x gptel-load-tools          ;; Load available tools
M-x gptel-tools               ;; Show available tools list
M-x gptel-cursor              ;; Send context + prompt from cursor
M-x gptel-reload             ;; Reload configuration
M-x gptel-toggle             ;; Enable/disable GPTel mode
```

### 2. **MCP Commands**

```bash
# Start MCP Hub server (in terminal)
mcp-hub start --backend ollama

# Or start individual MCP servers
mcp-hub start git-mcp
mcp-hub start filesystem-mcp
mcp-hub start blender-mcp
```

**Emacs-side**:

```elisp
M-x mcp-list-tools           ;; List tools
M-x mcp-call                 ;; Call selected tool
M-x mcp-toggle               ;; Enable/disable MCP
```

### 3. **Aider Commands**

```bash
aider .                       ;; Start aider in current dir
aider --model llama3.2       ;; Use specific model
aider --prompt "refactor git commit"
```

**In Emacs**: Enable Aider mode when in project:

```bash
aider .
```

### 4. **Ollama / ELLama Commands**

```bash
ollama run qwen2.5-coder:3b        ;; Run model
ollama list                         ;; List installed models
ollama show qwen2.5-coder          ;; Model info
```

### 5. **Pi-coding Commands**

```bash
pi-coding init                    ;; Initialize Pi coding environment
pi-coding analyze                 ;; Analyze project structure
pi-coding generate               ;; Generate code from spec
```

*(Note: Pi-coding might be a conceptual name; adapt to your specific coding assistant tools.)*

---

## Suggested Usage Patterns

### 1. **Quick Contextual Query**

```bash
# Type your question, then:
M-x gptel-cursor
```

**What it does**: Sends text from cursor to LLM; ideal for quick questions about code or context.

### 2. **Prompt from Selected Region**

```bash
# Select code region, then:
M-x gptel-region
```

**What it does**: Sends selected code + prompt to LLM for transformation/refactoring.

### 3. **Tool Call for Filesystem Operations**

```bash
# In GPTel buffer:
M-x mcp-call :tool=filesystem :action=read_file :path="~/project/file.py"
```

**What it does**: Uses MCP filesystem tool to read/write files without leaving Emacs.

### 4. **Git Operations via MCP**

```bash
M-x mcp-call :tool=git :action=commit :message="Fix pipeline config"
```

**What it does**: Commits Git changes through MCP Git tool.

---

## Suggested Workflow

### **Daily Workflow**

1. **Start Emacs**

   ```bash
   emacs ~/lav/src/blender_cv/mcp_server
   ```

2. **Enable Agentic Tools**

   ```elisp
   M-x gptel-load-and-call
   M-x mcp-toggle
   ```

3. **Type a Prompt**

   - Type your request in the minibuffer or selected buffer
   - Press **C-c C-g** (your GPTel keybinding)

4. **Review AI Response**

   - GPTel response appears in a dedicated buffer
   - Edit or accept patches as needed

5. **Use Tools**

   - File read/write: `filesystem` tool
   - Git operations: `git` tool
   - LLM chat: `ollama` tool
   - Execute shell commands: `shell` tool

6. **Apply Changes**

   - GPTel offers to load patches into buffers
   - Review diff before applying

### **Continuous Integration / Development**

1. **Start Development Session**

   ```bash
   # Enable all agentic tools
   M-x gptel-load-tools
   M-x mcp-toggle
   ```

2. **Let Aider Assist**

   ```bash
   # Start Aider in project root
   aider .
   ```

3. **Query LLM for Next Steps**

   - Select problematic code
   - Use `M-x gptel-cursor` to ask refactoring help
   - Or use GPTel region mode

4. **Run Tests / Build via Tools**

   - Use MCP filesystem to execute tests
   - Check logs and fix issues

5. **Commit Changes**

   ```bash
   M-x mcp-call :tool=git :action=commit
   ```

### **Pi-coding for Small Projects**

1. **Initialize Pi-coding**

   ```bash
   pi-coding init my-project
   ```

2. **Describe Requirements**

   - Use `pi-coding generate` with a spec
   - AI generates scaffolding

3. **Iterate**

   - Refine spec based on AI suggestions
   - Use GPTel for fine-tuning

4. **Deploy**

   - Review generated code
   - Commit to Git with MCP

---

## Suggested Commands Cheat Sheet

| Command | Purpose |
|---------|-------------|
| `M-x gptel-load-and-call` | Load and launch GPTel |
| `M-x gptel-send` | Send prompt to backend |
| `M-x gptel-cursor` | Send cursor context + prompt |
| `M-x gptel-region` | Send selected region |
| `M-x mcp-toggle` | Toggle MCP mode |
| `M-x mcp-call` | Call specific MCP tool |
| `M-x mcp-list-tools` | List available tools |
| `M-x aider` | Start Aider for code edits |
| `ollama run model` | Run local LLM |
| `M-x vertico-mode` | Activate minibuffer completion |
| `M-x recentf-mode` | Show recent files |

---

## Keybindings

Your `.emacs` file may include:

```elisp
(global-set-key (kbd "C-c C-g") 'gptel-load-and-call)   ;; GPTel main
(global-set-key (kbd "C-c C-m") 'mcp-toggle)             ;; Toggle MCP
(global-set-key (kbd "C-c C-t") 'mcp-call)               ;; Call MCP tool
```

---

## Troubleshooting

### If GPTel won't load

1. Check Ollama is running:

   ```bash
   ps aux | grep ollama
   ```

2. Ensure port is accessible:

   ```bash
   curl http://localhost:11434
   ```

### If MCP isn't responding

1. Check MCP server logs:

   ```bash
   tail -f /path/to/mcp-logs
   ```

2. Restart MCP process:

   ```bash
   mcp-hub restart
   ```

### If tools not visible

1. Run `M-x gptel-load-tools` again
2. Check your `gptel-use-tools` is `t`

---

## Advanced: Building Your Own Agentic System

### 1. **Define Custom Tools**

You can write custom Elisp functions that GPTel calls:

```elisp
(defun my/custom-tool ()
  "Custom tool that runs Blender simulation.")
(gptel-register-tool "blender-run" 'my/custom-tool)
```

### 2. **Chain Multiple Tools**

Use GPTel to orchestrate multiple tools in sequence:

```elisp
(gptel-send "1. Read file1
2. Run git diff
3. Show file2")
```

### 3. **Context-aware Agent**

Configure GPTel to keep conversation history across sessions:

```elisp
(setq gptel--converse-history t)
```

---

## Summary

| Tool | Best Used For |
|------|---------------|
| **GPTel** | Prompts, tool calls, quick queries |
| **MCP-Hub** | Centralised tool management |
| **Aider** | File editing with AI |
| **Ollama** | Local LLM hosting |
| **Pi-coding** | Personalised coding assistant (conceptual) |

---

## Next Steps

1. **Try GPTel region mode** – select code + ask refactoring
2. **Test MCP tools** – read/write files, commit Git
3. **Experiment with Aider** – AI-driven code edits
4. **Build a custom agent** – chain tools together

---

## Notes on `simple.el`

We mentioned that `simple.el` is **not loaded** in your Emacs config. This is why there's no conflict. Your agentic setup should run without issues.

If you ever want to enable `simple.el`, comment out the defensive lines in `emacs.el`. But they're unnecessary for typical GPTel/MCP workflows.

---

For more details, see `README.md` in this directory.