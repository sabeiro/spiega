#!/usr/bin/env bash
# Create SSL certificate and optional .htpasswd in $HOME/credenza for nginx in Docker.
# Run once, then start compose; nginx will use these via the credenza volume.

set -e
CREDENZA="${HOME}/credenza/ssl"
CERT_DAYS=3650
SUBJECT="/CN=jetson/O=Jetson/C=XX"

mkdir $HOME/credenza/ssl/
sudo apt install apache2-utils
#htpasswd -c /home/sab/credenza/ssl/.htpasswd webdav

mkdir -p "$CREDENZA"
cd "$CREDENZA"

if [[ -f jetson.key && -f jetson.crt ]]; then
  echo "Certificates already exist in $CREDENZA (jetson.key, jetson.crt)."
  read -p "Overwrite? [y/N] " -n 1 -r; echo
  if [[ ! $REPLY =~ ^[yY]$ ]]; then
    echo "Skipping certificate creation."
    exit 0
  fi
fi

echo "Creating self-signed certificate in $CREDENZA (valid ${CERT_DAYS} days)..."
openssl req -x509 -nodes -days "$CERT_DAYS" -newkey rsa:2048 \
  -keyout jetson.key -out jetson.crt \
  -subj "$SUBJECT" \
  -addext "subjectAltName=DNS:jetson,DNS:webui.jetson,DNS:ollama.jetson,IP:127.0.0.1"

chmod 600 jetson.key
chmod 644 jetson.crt
echo "Created: $CREDENZA/jetson.key, $CREDENZA/jetson.crt"

if [[ ! -f .htpasswd ]]; then
  echo "Creating .htpasswd for WebDAV (user: webdav). You will be prompted for a password."
  if command -v htpasswd &>/dev/null; then
    htpasswd -c .htpasswd webdav
  else
    echo "htpasswd not found. Create manually: htpasswd -c $CREDENZA/.htpasswd webdav"
    echo "Or on Debian/Ubuntu: sudo apt install apache2-utils"
  fi
else
  echo ".htpasswd already exists in $CREDENZA"
fi

echo "Done. Start nginx with: docker compose up -d nginx"
