# Ansible – webui basic operations

Rebuild, restart, start, or stop Docker Compose services (nginx, ollama, mcp) on the Jetson.

## Setup

- Ansible 2.9+ on the machine you run from.
- SSH access to the target host (or use `localhost` with `connection: local`).
- On the target: Docker and `docker compose` (v2), and the project at `webui_project_path` (see `group_vars/all.yml`).

## Inventory

Edit `inventory.yml` and set `ansible_host` (e.g. `ollama.jetson` or the Jetson IP) and `ansible_user`.  
To run on the same machine (project path must exist locally):

```yaml
all:
  hosts:
    jetson:
      ansible_host: 127.0.0.1
      ansible_connection: local
```

Set `webui_project_path` in `group_vars/all.yml` to the path where `docker-compose.yml` lives on the target.

## Usage

From the **ansible** directory (or pass the path to the playbook):

```bash
cd /home/gmare/mount/jetson/webui/ansible
```

**Rebuild** one service (build image + recreate container):

```bash
ansible-playbook -i inventory.yml playbook.yml -e "action=rebuild" -e "service=mcp"
```

**Rebuild** all services:

```bash
ansible-playbook -i inventory.yml playbook.yml -e "action=rebuild"
```

**Rebuild** without using cache:

```bash
ansible-playbook -i inventory.yml playbook.yml -e "action=rebuild" -e "service=mcp" -e "no_cache=true"
```

**Restart** one or all:

```bash
ansible-playbook -i inventory.yml playbook.yml -e "action=restart" -e "service=nginx"
ansible-playbook -i inventory.yml playbook.yml -e "action=restart"
```

**Start** / **Stop**:

```bash
ansible-playbook -i inventory.yml playbook.yml -e "action=start"
ansible-playbook -i inventory.yml playbook.yml -e "action=stop" -e "service=ollama"
```

**Logs** (e.g. mcp for latency debugging; default service=mcp, last 200 lines):

```bash
./run.sh logs
./run.sh logs mcp --tail 500
ansible-playbook -i inventory.yml playbook.yml -e "action=logs" -e "service=mcp" -e "logs_tail=500"
```

Agent logs are structured: `req_id`, `stage=...`, `duration_ms=...`. Set `MCP_AGENT_DEBUG=1` in the mcp service env or send `"debug": true` in the request payload for verbose lines.

At the end, the playbook runs `docker compose ps` and prints container status.
