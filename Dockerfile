# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

FROM python:3.13-slim-bookworm AS base

# Set the working directory to /app
WORKDIR /usr/src/app

COPY . /usr/src/app

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates wget zsh

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

FROM base AS development

# A cache mount can be used to improve performance across builds:
ENV UV_LINK_MODE=copy

# Install necessary packages: gcc, make, libc-dev, bash, curl, and openssh-client
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash curl gcc git libc-dev make openssh-client unzip wget zsh \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory to /app
WORKDIR /usr/src/app

# Install Oh My Zsh (if needed)
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Install oh-my-zsh:
# Uses "Spaceship" theme with some customization. Uses some bundled plugins and installs some more from github
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.5/zsh-in-docker.sh)" -- \
    -t https://github.com/denysdovhan/spaceship-prompt \
    -a 'SPACESHIP_PROMPT_ADD_NEWLINE="false"' \
    -a 'SPACESHIP_PROMPT_SEPARATE_LINE="false"' \
    -p git \
    -p ssh-agent \
    -p https://github.com/zsh-users/zsh-autosuggestions \
    -p https://github.com/zsh-users/zsh-completions

# Enable shell completions for `uv`
RUN echo 'eval "$(uv generate-shell-completion zsh)"' >> ~/.zshrc

# Enable shell completions for `uvx`
RUN echo 'eval "$(uvx generate-shell-completion zsh)"' >> ~/.zshrc

# Sync the project into a new environment, using the frozen lockfile
RUN --mount=type=cache,target=/root/.cache/uv uv sync

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #