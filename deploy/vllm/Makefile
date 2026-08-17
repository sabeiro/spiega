.PHONY: all run download start stop clean help

all: help

help:
	@echo ""
	@echo "=== vLLM Docker Compose Commands ==="
	@echo ""
	@echo "Usage:"
	@echo "  make help              - Show this help"
	@echo "  make start             - Start vLLM service"
	@echo "  make stop              - Stop vLLM service"
	@echo "  make rm                - Remove vLLM container"
	@echo "  make clean             - Remove containers, volumes, images"
	@echo "  make reset             - Full reset (stop, rm, clean)"
	@echo "  make download          - Download llama-3.1-8b-instruct model"
	@echo "  make init              - Setup (directories + make executable)"
	@echo ""
	@echo "Example commands:"
	@echo "  make init && make download"
	@echo "  make download"
	@echo "  make init && make start"
	@echo "  make start && make download"
	@echo "  make start && make download && make stop"
	@echo ""
	@echo "=== Model Info ==="
	@echo "Model: llama-3.1-8b-instruct"
	@echo "Download: ./models/llama-3.1-8b-instruct/"
	@echo ""

init:
	@echo "=== Initializing vLLM setup ==="
	@mkdir -p models cache
	@chmod +x download_model.sh
	@echo "Setup complete."

start:
	@echo "=== Starting vLLM ==="
	@docker-compose up -d

stop:
	@echo "=== Stopping vLLM ==="
	@docker-compose down

rm:
	@echo "=== Removing container ==="
	@docker-compose rm -f vllm

clean:
	@echo "=== Cleaning containers, volumes, images ==="
	@docker-compose down
	@docker-compose rm -f
	@docker volume rm mcp_server_vllm_cache

reset: stop rm clean
	@echo "=== Full reset complete ==="
	@make init

download:
	@echo "=== Downloading model ==="
	@./download_model.sh
