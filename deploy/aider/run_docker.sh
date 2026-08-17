docker pull paulgauthier/aider
docker run -it --user $(id -u):$(id -g) --volume $(pwd):/app paulgauthier/aider --openai-api-key $OPENAI_API_KEY [...other aider args...]

