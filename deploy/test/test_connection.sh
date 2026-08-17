#!/usr/bin/env bash
# Test POST /mcp/api/chat via agent. Logs in nginx-style with response time; backs up
# docker-compose.yml on success. Uses a writable log path (default /tmp).
set -e
QUESTION="What time it is?"
QUESTION="2+2?"
#QUESTION="What is ollama?"
HOST_LLM="${HOST_LLM:--k https://ollama.jetson}"
MODEL="${OLLAMA_MODEL:-qwen2.5-coder:3b}"
# MODEL="${OLLAMA_MODEL:-llama3.2:1b}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"
LOG_FILE="${TEST_CONNECTION_LOG:-${TMPDIR:-/tmp}/webui-test-connection.log}"
BACKUP_DIR="${PROJECT_ROOT}/backup"
# ISO 8601 timestamp for log
TIME_LOCAL="$(date -Iseconds)"

mkdir -p "$BACKUP_DIR" 2>/dev/null || true

log_line() { echo "$*" >> "$LOG_FILE"; }

echo "=== POST /mcp/api/chat (via agent) ==="
echo "Model: $MODEL  Time: $TIME_LOCAL"
echo ""

# Use delimiter so we can parse body vs metadata (body may contain newlines)
CURL_DELIM="---CURL_METADATA---"
# Set DEBUG=1 or pass --debug to enable agent verbose logging (options.debug in payload).
DEBUG="${DEBUG:-0}"
[[ " $* " = *" --debug "* ]] && DEBUG=1
OPT_DEBUG=""
[[ "$DEBUG" = "1" ]] && OPT_DEBUG=', "debug": true'
RESPONSE="$(curl -s -w "${CURL_DELIM}%{http_code}${CURL_DELIM}%{time_total}${CURL_DELIM}%{size_download}" $HOST_LLM/mcp/api/chat -X POST -H "Content-Type: application/json" -d '{
  "model": "'"$MODEL"'",
  "messages": [{"role": "user", "content": "'$QUESTION'"}],
  "options": {"log_response": true, "seed": 101, "num_gpu": 20, "temperature": 0'"$OPT_DEBUG"'}
}')"
HTTP_BODY="${RESPONSE%%${CURL_DELIM}*}"
REST="${RESPONSE#*${CURL_DELIM}}"
HTTP_CODE="${REST%%${CURL_DELIM}*}"
REST="${REST#*${CURL_DELIM}}"
TIME_TOTAL="${REST%%${CURL_DELIM}*}"
SIZE_DOWNLOAD="${REST#*${CURL_DELIM}}"

# Nginx-style line with ISO date: remote - user timestamp "request" status body_bytes_sent "referer" "user_agent" request_time extra
# Example: - - 2026-02-17T14:45:50+01:00 "POST /api/chat HTTP/1.1" 200 1234 "-" "test_connection.sh" 9.164 model=qwen2.5-coder:3b
LOG_LINE="- - ${TIME_LOCAL} \"POST /mcp/api/chat HTTP/1.1\" ${HTTP_CODE} ${SIZE_DOWNLOAD} \"-\" \"test_connection.sh\" ${TIME_TOTAL} model=${MODEL}"
log_line "$LOG_LINE"
echo "$HTTP_BODY"
printf "\n"

# Success: 200 and no top-level "error" in JSON
SUCCESS=0
if [[ "$HTTP_CODE" == "200" ]]; then
  if echo "$HTTP_BODY" | grep -q '"error"'; then
    ERR="$(echo "$HTTP_BODY" | sed -n 's/.*"error"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)"
    log_line "# result=error_in_body error=${ERR}"
  else
    SUCCESS=1
  fi
else
  log_line "# result=fail http_code=${HTTP_CODE}"
fi

if [[ "$SUCCESS" -eq 1 ]]; then
  BACKUP_NAME="docker-compose-$(date +%Y%m%d-%H%M%S).yml"
  BACKUP_PATH="${BACKUP_DIR}/${BACKUP_NAME}"
  if [[ -f "${PROJECT_ROOT}/docker-compose.yml" ]]; then
    rm "$BACKUP_DIR"/*.yml 2>/dev/null || true
    if cp "${PROJECT_ROOT}/docker-compose.yml" "$BACKUP_PATH" 2>/dev/null; then
      log_line "# backup=${BACKUP_PATH}"
      echo "Success: backed up docker-compose.yml to ${BACKUP_PATH}"
    else
      log_line "# backup=skipped (not writable: ${BACKUP_DIR})"
      echo "Success (backup skipped: ${BACKUP_DIR} not writable)"
    fi
  fi
fi

echo "Log written to ${LOG_FILE} (response_time=${TIME_TOTAL}s)"

exit $((1 - SUCCESS))
