#!/usr/bin/env zsh

# **************************************************************************************

# @package        @lumispace/common
# @license        Copyright © 2021-2025 Lumi.Space

# **************************************************************************************

# Enable strict error handling
set -euo pipefail

# **************************************************************************************

# Variables
CONFIG_FILE="ruff.toml"
DIRECTORY="."
LOG_FILE="ruff_formatter.log"

# **************************************************************************************

# Import all shared functions from common.sh
SCRIPT_DIR="$(cd "$(dirname "${(%):-%N}")" && pwd)"
COMMON_SCRIPT="$SCRIPT_DIR/common.sh"

if [[ ! -f "$COMMON_SCRIPT" ]]; then
    echo "Error: 'common.sh' not found in '$SCRIPT_DIR'. Please ensure it exists." >&2
    exit 1
fi

source "$COMMON_SCRIPT"

# **************************************************************************************

# Parse command-line arguments
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

# Start logging
exec > >(tee -i "$LOG_FILE") 2>&1

echo "Starting code formatting with ruff..."
echo "Configuration file: $CONFIG_FILE"
echo "Target directory: $DIRECTORY"

# **************************************************************************************

# Check if 'uvx' command is available
check_command "uvx"

# **************************************************************************************

# Check if 'ruff' is available through 'uvx'
if ! uvx ruff --version >/dev/null 2>&1; then
    error_exit "'ruff' is not available via 'uvx'. Please ensure 'ruff' is installed in your environment."
fi

# **************************************************************************************

# Check if configuration file exists
if [[ ! -f "$CONFIG_FILE" ]]; then
    error_exit "Configuration file '$CONFIG_FILE' not found in the current directory."
fi

# **************************************************************************************

# Run the formatter
if ! uvx ruff format "$DIRECTORY" --config "$CONFIG_FILE"; then
    error_exit "Formatting failed. Please check the errors above and try again."
fi

# **************************************************************************************

echo "Formatting complete. Logs are available in '$LOG_FILE'."

# **************************************************************************************