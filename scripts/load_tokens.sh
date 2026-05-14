#!/usr/bin/env bash
# Source this file before running publish/upload scripts to populate API tokens
# from the local secret-store without ever printing them to stdout or logs.
#
# Usage:
#   source scripts/load_tokens.sh
#   python3 scripts/whatever_uses_zenodo.py
#
# Reads ~/.config/vera-secrets/values/<namespace>.env (KEY=VALUE format) and
# exports each KEY into the current shell. Never echoes a value.
#
# Note on GitHub:
#   Routine git operations against GitHub use the SSH key configured for the
#   `gh` CLI; no PAT is required. A PAT would only be needed for HTTPS API
#   automation paths (release asset upload, programmatic webhook/secret
#   management, etc.) which this project does not currently use. If such a
#   path is ever needed, store a *minimum-scope* PAT under github.env and it
#   will be loaded automatically.

set -u

_secrets_dir="${HOME}/.config/vera-secrets/values"

_load_secret_namespace() {
    local namespace="$1" envfile required="${2:-required}"
    envfile="${_secrets_dir}/${namespace}.env"
    if [[ -r "$envfile" ]]; then
        set -a
        # shellcheck disable=SC1090
        source "$envfile"
        set +a
        return 0
    fi
    if [[ "$required" == "required" ]]; then
        echo "warning: ${namespace}.env not found in secret-store" >&2
    fi
    return 1
}

_load_secret_namespace zenodo required
_load_secret_namespace github optional

unset _secrets_dir _load_secret_namespace
