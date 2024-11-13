#!/usr/bin/env zsh

# **************************************************************************************

# @package        @lumispace/common
# @license        Copyright © 2021-2025 Lumi.Space

# **************************************************************************************

# Enable strict error handling
set -euo pipefail

# **************************************************************************************
 
SCRIPT_DIR="$(cd "$(dirname "${(%):-%N}")" && pwd)"
COMMON_SCRIPT="$SCRIPT_DIR/common.sh"

if [[ ! -f "$COMMON_SCRIPT" ]]; then
    echo "Error: 'common.sh' not found in '$SCRIPT_DIR'. Please ensure it exists." >&2
    exit 1
fi

source "$COMMON_SCRIPT"

# **************************************************************************************

CONFIG_FILE="pyproject.toml"
DIRECTORY="."
LOG_FILE="pytest.log"

# **************************************************************************************

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

# **************************************************************************************

exec > >(tee -i "$LOG_FILE") 2>&1

echo "Starting code testing with pytest..."
echo "Configuration file: $CONFIG_FILE"
echo "Target directory: $DIRECTORY"

# **************************************************************************************

check_command "uv"
check_command "pytest"

# **************************************************************************************

if [[ ! -f "$CONFIG_FILE" ]]; then
    error_exit "Configuration file '$CONFIG_FILE' not found in the current directory."
fi

# **************************************************************************************

echo "Running pytest with uv..."

if ! uv run --link-mode=copy pytest "$DIRECTORY"; then
    error_exit "Testing failed. Please check the errors above and try again."
fi

# **************************************************************************************

echo "Testing complete. Logs are available in '$LOG_FILE'."

# **************************************************************************************