#!/usr/bin/env zsh

# **************************************************************************************

# @package        @lumispace/common
# @license        Copyright © 2021-2025 Lumi.Space

# **************************************************************************************

# Function to display error messages and exit
error_exit() {
    echo "Error: $1" >&2
    exit 1
}

# **************************************************************************************

# Function to display help
show_help() {
    echo "Usage: $(basename "$0") [options]"
    echo
    echo "Options:"
    echo "  -h, --help            Show this help message and exit"
    echo "  -c, --config FILE     Specify a custom configuration file (default: ruff.toml)"
    echo "  -d, --directory DIR   Specify the directory to lint/format (default: current directory)"
    echo
    echo "Example:"
    echo "  $(basename "$0") --config custom_ruff.toml --directory projects/"
}

# **************************************************************************************

# Function to check if a command exists
check_command() {
    if ! command -v "$1" >/dev/null 2>&1; then
        error_exit "'$1' command not found. Please install '$1' and try again."
    fi
}

# **************************************************************************************