#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# Helper function to check commands
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Detect distro
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
else
    echo "Unsupported Linux distribution."
    exit 1
fi

# Ensure script runs as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root or with sudo."
    exit 1
fi

echo "Detected Linux distro: $DISTRO"

install_docker_ubuntu_debian() {
    echo "==> Updating packages..."
    apt update -y
    apt install -y ca-certificates curl gnupg lsb-release

    mkdir -p /etc/apt/keyrings
    if [ ! -f /etc/apt/keyrings/docker.gpg ]; then
        echo "==> Adding Docker GPG key..."
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
        chmod a+r /etc/apt/keyrings/docker.gpg
    fi

    DOCKER_REPO_FILE="/etc/apt/sources.list.d/docker.list"
    if [ ! -f "$DOCKER_REPO_FILE" ]; then
        echo "==> Adding Docker repository..."
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" > "$DOCKER_REPO_FILE"
    fi

    echo "==> Installing Docker packages..."
    apt update -y
    apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
}

install_docker_fedora_rhel() {
    echo "==> Installing required packages..."
    dnf install -y dnf-plugins-core

    echo "==> Adding Docker repository..."
    if ! dnf repolist | grep -q docker; then
        dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
    fi

    echo "==> Installing Docker packages..."
    dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
}

install_docker_arch() {
    echo "==> Updating packages..."
    pacman -Sy --noconfirm

    echo "==> Installing Docker packages..."
    pacman -S --noconfirm docker docker-compose
}

# Install Docker based on distro
case "$DISTRO" in
    ubuntu|debian)
        install_docker_ubuntu_debian
        ;;
    fedora|rhel|centos)
        install_docker_fedora_rhel
        ;;
    arch)
        install_docker_arch
        ;;
    *)
        echo "Unsupported Linux distribution: $DISTRO"
        exit 1
        ;;
esac

echo "==> Enabling and starting Docker service..."
systemctl enable docker
systemctl start docker
systemctl status docker --no-pager

echo "==> Adding current user to the Docker group..."
usermod -aG docker "${SUDO_USER:-$USER}"

echo "==> Refreshing group membership..."
newgrp docker <<EOF
echo "==> Building Docker image..."
docker build -t fahrgemeinschaften .

echo "==> Starting Docker Compose services..."
docker compose up -d
EOF

echo "==> Docker installation and setup completed successfully!"
