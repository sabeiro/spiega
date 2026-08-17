# Complete Emacs Project Packages Documentation

This document lists all Emacs packages used in the project, their purposes, and recommendations for removal.

---

## Main Custom Config Files

### 1. **ede-projects.el** (4 lines)

| Aspect | Details |
|--------|---------|
| **Purpose** | EDE (Emacs Data Environment) project management. |
| **Used** | Loads `.ede` project files. |
| **Can Remove** | **YES** if you don't use EDE for project management. |
| **Status** | Minimal; safe to comment out. |

---

### 2. **start_slack.el** (52 lines)

| Aspect | Details |
|--------|---------|
| **Purpose** | Slack integration in Emacs. |
| **Used** | Connects to Slack workspace. |
| **Can Remove** | **YES** if you don't use Slack or prefer other chat. |
| **Status** | Small; remove if not actively using Slack. |

---

### 3. **json-mode.el** (222 lines) |

| Aspect | Details |
|--------|---------|
| **Purpose** | Built-in JSON editing mode. |
| **Used** | Editing JSON configs (e.g., `.json`). |
| **Can Remove** | **NO** – built-in to Emacs; required. |
| **Status** | Keep – essential for config files. |

---

### 4. **json.el** (530 lines) |

| Aspect | Details |
|--------|---------|
| **Purpose** | Custom JSON manipulation functions. |
| **Used** | Complex JSON operations, conversion between formats. |
| **Can Remove** | **Conditional** – remove if you only need basic JSON support. |
| **Status** | Keep if using advanced JSON. |

---

### 5. **nodejs-repl.el** (501 lines) |

| Aspect | Details |
|--------|---------|
| **Purpose** | Node.js REPL integration. |
| **Used** | Running Node.js code interactively from Emacs. |
| **Can Remove** | **YES** if you prefer running Node.js externally or via MCP tools. |
| **Status** | Remove if you only use Node.js through MCP or external scripts. |

---

## Python Packages

### 6. **python-mode.el** (27,559 lines) |

| Aspect | Details |
|--------|---------|
| **Purpose** | Complete Python editing in Emacs. |
| **Used** | Syntax highlighting, refactoring, linting, debugging. |
| **Can Remove** | **NO** – only way to edit Python in Emacs. |
| **Status** | **Keep** – essential for Python development. |
| **Notes** | Requires Python + pip packages (e.g., `pyright`, `black`, `flake8`). |

---

## HTML/CSS/JS Packages

### 7. **web-mode.el** (11,671 lines) |

| Aspect | Details |
|--------|---------|
| **Purpose** | Multi-language web editor (HTML, CSS, JS, TS, etc.). |
| **Used** | Editing web frontend files in one package. |
| **Can Remove** | **NO** – only way to edit web files cleanly. |
| **Status** | **Keep** – essential for web development. |
| **Features** | Live reload, JSX support, CSS preprocessor support. |

---

### 8. **web-beautify.el** (188 lines) |

| Aspect | Details |
|--------|---------|
| **Purpose** | Formats/minifies web code beautification. |
| **Used** | Indent/formatting HTML/CSS/JS. |
| **Can Remove** | **Optional** – can use external tools (e.g., Prettier). |
| **Status** | Remove if you prefer external formatters. |

---

### 9. **js-comint.el** (429 lines) |

| Aspect | Details |
|--------|---------|
| **Purpose** | Shell completion for JavaScript/Node.js. |
| **Used** | Running Node.js scripts from buffer. |
| **Can Remove** | **YES** if you use MCP tools for shell execution. |
| **Status** | Remove if you only use MCP for shell. |

---

### 10. **yaml-mode.el** (441 lines) |

| Aspect | Details |
|--------|---------|
| **Purpose** | YAML editing support. |
| **Used** | Editing YAML configs (Docker, K8s, etc.). |
| **Can Remove** | **NO** – essential for YAML editing. |
| **Status** | Keep – required for infrastructure configs. |

---

## Summary Table

| File | Lines | Purpose | Can Remove? | Recommendation |
|------|-------|---------|-------------|----------------|
| **ede-projects.el** | 4 | EDE project loading | ✅ Yes | Only remove if not using EDE |
| **start_slack.el** | 52 | Slack integration | ✅ Yes | Remove if no Slack |
| **json-mode.el** | 222 | JSON editing mode | ❌ No | Keep – built-in |
| **json.el** | 530 | Advanced JSON | ⚠️ Conditional | Remove if not needed |
| **nodejs-repl.el** | 501 | Node REPL | ✅ Yes | Remove if no Node REPL |
| **python-mode.el** | 27,559 | Python editing | ❌ No | **Keep – essential** |
| **web-mode.el** | 11,671 | Web frontend editing | ❌ No | **Keep – essential** |
| **web-beautify.el** | 188 | Code beautification | ⚠️ Optional | Remove if using Prettier |
| **js-comint.el** | 429 | JS shell completion | ✅ Yes | Remove if using MCP |
| **yaml-mode.el** | 441 | YAML editing | ❌ No | Keep for YAML configs |

---

## Recommended Cleanup Steps

### Step 1: Identify Unused Packages

Run this command in Emacs:

```elisp
M-x list-packages          ;; List installed packages
M-x find-file /path/to/file ;; Check what each does
```

### Step 2: Remove or Comment Out

1. **Safe to remove**:
   - `ede-projects.el` (if not using EDE)
   - `start_slack.el` (if no Slack need)
   - `nodejs-repl.el` (if using MCP tools)
   - `js-comint.el` (if using MCP shell)
   - `web-beautify.el` (if using Prettier)

2. **Keep**:
   - `python-mode.el` (essential for Python)
   - `web-mode.el` (essential for web)
   - `json-mode.el` (built-in, keep)
   - `yaml-mode.el` (essential for YAML)

3. **Conditional**:
   - `json.el` (advanced JSON functions)
   - `web-beautify.el` (external formatter preferred)

---

## External Tool Integration

If you're using external tools, you can remove internal Emacs counterparts:

| External Tool | Removes Emacs Package |
|---------------|-------------- |
| Prettier | `web-beautify.el` |
| MCP shell tools | `js-comint.el`, `nodejs-repl.el` |
| EDE | `ede-projects.el` |
| External Slack client | `start_slack.el` |

---

## Python Packages

Your Python files use:

- **pyright** – Type checking
- **black** – Code formatting (can replace `web-beautify.el`)
- **flake8** – Linting

**Recommendation**: Use external tools for Python formatting – remove internal beautify.

---

## Web Packages

Your project uses:

- **web-mode.el** → HTML/CSS/JS/TS editing
- **external** → Prettier for formatting

**Recommendation**: Keep `web-mode.el`, remove `web-beautify.el` if using Prettier.

---

## Node.js Packages

Your Node.js files use:

- **nodejs-repl.el** → REPL for Node.js
- **js-comint.el** → Shell completion

**Recommendation**: If you use MCP for shell, remove both.

---

## Summary

**Keep**:

- `python-mode.el` – Only Python editor in Emacs
- `web-mode.el` – Only web frontend editor
- `json-mode.el` – Built-in JSON support
- `yaml-mode.el` – YAML editing
- `ede-projects.el` (if using EDE)

**Remove**:

- `nodejs-repl.el` – Use MCP for shell
- `js-comint.el` – Use MCP for shell
- `start_slack.el` – If not using Slack
- `web-beautify.el` – Use Prettier instead

**Conditional**:

- `json.el` – Advanced JSON functions (remove if not using)

---

## Next Steps

1. Run `list-packages` in Emacs
2. Try commenting out "remove" packages
3. Test that you can still edit files correctly
4. If works, remove from config permanently

---

## Notes on `simple.el`

We mentioned that `simple.el` is **not loaded** in your Emacs config. This is why there's no conflict. Your agentic setup should run without issues.

If you ever want to enable `simple.el`, comment out the defensive lines in `emacs.el`. But they're unnecessary for typical GPTel/MCP workflows.

---

For complete context, see both `README.md` and `AGENTIC_USAGE.md` in this directory.