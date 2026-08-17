# Start from a minimal Ubuntu base image
FROM ubuntu:22.04

# Install Python, pip, and build tools required for vLLM
RUN apt update && \
    apt install -y python3 python3-pip wget git cmake build-essential

# Upgrade pip to ensure the latest package compatibility
#RUN pip3 upgrade --user 

# Set environment variables for internal container use
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
VOLUME /home/sabeiro/Downloads/llm_model/ /model/
WORKDIR /app

# Install vLLM and other required dependencies (This is the key step)
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy a simple entrypoint script to run the server
COPY start_server.sh .

RUN chmod u+x start_server.sh
# Define the command to run when the container starts
#ENTRYPOINT ["/bin/bash", "/app/start_server.sh"]
