#!/usr/bin/env bash
# Source this file before running publish/upload scripts to populate API tokens
# from the local secret-store without ever printing them to stdout or logs.
#
# Usage:
#   source scripts/load_tokens.sh
#   python3 scripts/whatever_uses_zenodo_or_github.py
#
# Reads ~/.config/vera-secrets/values/<namespace>.env (KEY=VALUE format) and
# exports each KEY into the current shell. Never echoes a value.

set -u

_secrets_dir="${HOME}/.config/vera-secrets/values"

_load_secret_namespace() {
    local namespace="$1" envfile
    envfile="${_secrets_dir}/${namespace}.env"
    if [[ -r "$envfile" ]]; then
        set -a
        # shellcheck disable=SC1090
        source "$envfile"
        set +a
        return 0
    fi
    return 1
}

_load_secret_namespace github  || echo "warning: github.env not found in secret-store"  >&2
_load_secret_namespace zenodo  || echo "warning: zenodo.env not found in secret-store"  >&2

unset _secrets_dir _load_secret_namespace
