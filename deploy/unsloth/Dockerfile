# ========== Ubuntu 26.04 + python3 + unsloth studio ==========

FROM ubuntu:latest
SHELL ["/bin/bash", "-c"]
RUN curl -fsSL https://unsloth.ai/install.sh | bash -s -- --no-prompt
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONPATH="/root/.local/lib:$PYTHONPATH"
ENV UNSLOTH_STUDIO_HOME=/home/sabeiro/.unsloth/studio
# Basic dependencies
RUN apt-get update && apt-get install -y build-essential curl git
RUN apt-get install -y emacs vim npm nodejs
# Upgrade pip
# RUN python3 -m pip install --ignore-installed --upgrade pip --break-system-packages

#RUN curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-prompt --no-onboard
RUN curl -fsSL https://pi.dev/install.sh |  bash -s -- --no-prompt --no-onboard
#RUN curl -fsSL https://opencode.ai/install | bash -s -- --no-prompt --no-onboard
#RUN curl -LsSf https://aider.chat/install.sh | bash -s -- 

#RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# ARG UID=1000
# ARG GID=1000
# RUN usermod -l sabeiro ubuntu
# RUN usermod -d /home/sabeiro/ sabeiro
# RUN usermod -s /bin/bash sabeiro
# RUN groupadd sabeiro	 
# RUN usermod -aG ubuntu sabeiro
# RUN usermod -aG sabeiro sabeiro
# RUN mkdir -p /home/sabeiro/lav/src/
# RUN chown -R sabeiro:sabeiro /home/sabeiro/
# USER sabeiro

#CMD ["unsloth", "studio", "--host=0.0.0.0", "--port=8888"]
