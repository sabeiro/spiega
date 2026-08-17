# Project: llama_cpp agent instructions

## Stack
- python
- docker
- blender
- fenics
- ollama

## ⚠️ Behavior Rules (DO NOT RUSH)
- Don't touch Ollama without explicit permission
- Don't download models without checking model_list.txt first
- Read existing scripts/app/ files before modifying
- Don't modify config files without permission
- Don't rush or over-explain limitations
- Remember Ctrl+C stops everything (no pause capability)
- If going wrong: just say "STOP" / "Wrong direction"

## 📥 GGUF Models without HF Token
Use direct HF URLs - don't rush downloading:
- llama-3.1-8b-instruct
- llama-3.2-3b-instruct
- llama-3.3-70b-instruct
- mistral-7b-v0.3
- phi-3-mini-4k
- qwen2.5-7b-instruct

Scripts in app/:
- app/download_model.sh
- app/download_gguf.sh
- app/get_gguf_without_token.sh
- app/setup.sh
- app/run.sh
- app/config.ini

## 🎯 Stop Commands
- Ctrl+C ← Kills process (no pause)
- "STOP" / "STOP" / "STOP" ← I pause responding
- "Wrong direction" / "Reset" ← I redirect immediately

## Use AGENTS.md from /home/sabeiro/.pi/agent/

## AGENTS.md merged content from /home/sabeiro/lav/src/blender_cv/mcp_server/AGENTS.md

# mcp configuration for local assistant

## Stack
- python
- docker
- blender
- fenics

## Rules
- We need assistants to quickly prototype and explore in robotics, 3d, computer vision
- Use existing patterns from src/ — don't invent new abstractions
- Simple editable code, not meant for abstraction or production
- Produce professional, clear documentation (web pages, slides)
- Don't rush or over-explain limitations

# Project scope

This project allows running local agents as supporters. Those agents will be used for:
- Supporting FEM/blender integration
- Energy optimization engines
- CV/ML on embedded devices

- goal :: a local coding assistant
- stack :: IDE: emacs, LLM serve: ollama, OS: ubuntu 26
- workflow :: within emacs, code executed via python REPL and .org code blocks
- purpose :: data analytics, no need for production code, simple and readable, avoid abstraction
- test :: no successful results without testing and documenting
- language :: English, don't translate
- config :: python programs use JSON files as config, run logs saved to runs/ folder

# project structure

Project structure:

- assistants :: coding assistants
  - [[./agent_call.org][agent_call.org]] :: detailed agent instructions
  - [[./aider/][aider/]] :: conf files to use with aider
  - [[./config.json][config.json]] :: the pi-coding-agent config file
  - [[./emacs][emacs]] :: conf files for agentic usage of emacs in org mode
- deployment ::
  - [[./ansible/][ansible/]] :: ansible script for remote deployment (jetson)
  - [[./docker-compose.yml][docker-compose.yml]] :: start mcp_server and mcp_client
  - [[./logs/][logs/]] :: application outputs for debugging
  - [[./nginx/][nginx/]] :: web server configuration (jetson)
  - [[./ollama/][ollama/]] :: ollama container and conf
  - [[./mcphub/][mcphub/]] :: to monitor mcp applications
  - [[./morpheus/][morpheus/]] :: nvidia onnx cybersecurity ML enrichment on cuda
  - [[./test/][test/]] :: collection of scripts to test configurations
- apps ::
  - [[./blender_mcp/][blender_mcp]] :: mcp addon for blender
  - [[./mcp-client/][mcp-client]] :: app to interact with mcp-server
  - [[./mcp-server/][mcp-server/]] :: app exposing mcp tools for language models
- context ::
  - [[./doc/][doc/]] :: machine generated documentation
- presentation ::
  - [[./html/][html]] :: slides and diagrams
  - [[./icon][icon/]] :: useful icons for presentation
  - [[./img/][img/]] :: images for documentation
  - [[./html/js/][js/]] :: javascript for presentation
  - [[./html/css/][css/]] :: style sheets
  - [[./data/][data/]] :: input data like json graphs
  - [[./script/][script/]] :: collection of scripts

# agent

- local :: developing local applications for pilot test, no over-engineering
- docker :: applications run locally or in docker, no virtual env needed

# project outcome

This project provides agentic support to data scientists. LLMs run locally with ollama on:
- ubuntu with Nvidia GPU
- Acer nitro V16 AI laptop (AMD Ryzen 7, RTX 5060, 32GB RAM)
- Nvidia Jetson orin nano (ARM Cortex-A55, 8GB RAM)

The data scientists need to build an MCP server to allow their programming to interact with:
- [[blender-mcp/][blender-mcp/]] :: blender for 3d modeling
- [[../heat_fem/][heat_fem/]] :: fenics/doplhin for FEM calculation
- [[../phys_opt][phys_opt]] :: optimization engine for graphs
- [[../pose_estimate_py][pose_estimate_py]] :: computer vision (pose estimate)
- knowledge graphs

# AGENTS.md merged from /home/sabeiro/.pi/agent/AGENT.md

# web/UI specs

Web pages should be produced with:
- Audience :: scientific/technical blog
- Theme :: dark, elegant, simple, readable
- Layout :: centered, collapsable long sections
- CSS :: use classes for styled sheets
- JS :: minimal usage, ideally none
- images :: centered with opaque background and shadow
- headers :: h1/h2/h3 should have similar shades but different
- navbar :: minimal, few links, elegant, discrete
- printable :: able to produce pdf, no button
- footer :: intertino as owner, CC by-nc-sa license

# tech stack

Main libraries:
- python: ollama, mcp
- js: d3.js
- web: html/css

# Hardware

The project is optimized to run locally on:
1. **Laptop (ACER nitro V16 AI)**:
   - CPU: AMD Ryzen 7 with NPU
   - GPU: NVIDIA GeForce RTX 5060
   - RAM: 32GB
2. **Nvidia Jetson Orin Nano**:
   - 2x ARM Cortex-A55 cores
   - RAM: 8GB

# License

CC by-nc-sa [[https://creativecommons.org/licenses/by-nc-sa/4.0/][CC by-nc-sa]]
