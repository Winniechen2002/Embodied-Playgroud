#!/usr/bin/env bash
# Launch the unchanged Isaac Sim standalone binary from a separate Python venv.
set -eo pipefail
agentbench_launcher_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
: "${ISAACSIM_PATH:?Set ISAACSIM_PATH to the extracted Isaac Sim 5.1 directory}"
: "${AGENTBENCH_ISAAC_PYTHON:?Set AGENTBENCH_ISAAC_PYTHON to the isolated Python 3.11 executable}"
if [[ ! -f "$ISAACSIM_PATH/setup_conda_env.sh" || ! -f "$ISAACSIM_PATH/VERSION" ]]; then
    echo 'The standalone Isaac Sim directory is incomplete.' >&2
    exit 2
fi
if [[ "$(head -c 5 "$ISAACSIM_PATH/VERSION")" != '5.1.0' ]]; then
    echo 'This launcher is pinned to Isaac Sim 5.1.0.' >&2
    exit 2
fi
# Do not inherit an unrelated developer PYTHONPATH.
unset PYTHONPATH
source "$ISAACSIM_PATH/setup_conda_env.sh"
# The isolated environment owns general Python dependencies. The binary supplies
# Kit, USD and its native extensions; its older HTTP dependencies must not shadow
# the explicitly resolved FastAPI/Starlette combination.
agentbench_isaac_site=$("$AGENTBENCH_ISAAC_PYTHON" -I -c 'import sysconfig; print(sysconfig.get_path("purelib"))')
export AGENTBENCH_ISAAC_BINARY=1
export PYTHONPATH="$agentbench_launcher_root/scripts/isaac_binary_bootstrap:$agentbench_isaac_site${PYTHONPATH:+:$PYTHONPATH}"
# No automatic EULA acceptance. The operator supplies any vendor acceptance flag.
exec "$AGENTBENCH_ISAAC_PYTHON" "$@"
