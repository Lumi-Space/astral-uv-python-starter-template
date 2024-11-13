#!/usr/bin/env zsh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${(%):-%N}")" && pwd)"
COMMON_SCRIPT="$SCRIPT_DIR/common.sh"

if [[ ! -f "$COMMON_SCRIPT" ]]; then
    echo "Error: 'common.sh' not found in '$SCRIPT_DIR'. Please ensure it exists." >&2
    exit 1
fi

source "$COMMON_SCRIPT"

CONFIG_FILE="mypy.ini"
DIRECTORY="."
LOG_FILE="mypy_type_checker.log"

while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            show_help
            exit 0
            ;;
        -c|--config)
            if [[ $# -lt 2 ]]; then
                error_exit "Option '$1' requires an argument."
            fi
            CONFIG_FILE="$2"
            shift 2
            ;;
        -d|--directory)
            if [[ $# -lt 2 ]]; then
                error_exit "Option '$1' requires an argument."
            fi
            DIRECTORY="$2"
            shift 2
            ;;
        *)
            error_exit "Unknown option: $1"
            ;;
    esac
done

exec > >(tee -i "$LOG_FILE") 2>&1

echo "Type checking with mypy..."
echo "Configuration file: $CONFIG_FILE"
echo "Target directory: $DIRECTORY"

check_command "uvx"

if ! uvx mypy --version >/dev/null 2>&1; then
    error_exit "'mypy' is not available via 'uvx'. Please ensure 'mypy' is installed in your environment."
fi

if [[ ! -f "$CONFIG_FILE" ]]; then
    error_exit "Configuration file '$CONFIG_FILE' not found in the current directory."
fi

if ! uvx mypy "$DIRECTORY" --config "$CONFIG_FILE" --explicit-package-bases; then
    error_exit "Type checking failed. Please fix the issues and try again."
fi

echo "Type checking complete. Logs are available in '$LOG_FILE'."