#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS_DIR="$ROOT_DIR"
ROS_DISTRO="${ROS_DISTRO:-jazzy}"

if [[ ! -f "/opt/ros/$ROS_DISTRO/setup.bash" ]]; then
  echo "ROS 2 $ROS_DISTRO introuvable: /opt/ros/$ROS_DISTRO/setup.bash"
  exit 1
fi

source "/opt/ros/$ROS_DISTRO/setup.bash"

for cmd in rosdep colcon ros2; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Commande manquante: $cmd"
    exit 1
  fi
done

python3 - <<'PY'
import importlib.util
import subprocess
import sys

missing = []
for module, pkg in [
    ("cerebras.cloud.sdk", "cerebras-cloud-sdk"),
    ("piper", "piper-tts"),
    ("simpleaudio", "simpleaudio"),
]:
    if importlib.util.find_spec(module) is None:
        missing.append(pkg)

if missing:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", *missing])
PY

if [[ ! -d "$WS_DIR/src" ]]; then
  echo "Workspace invalide: $WS_DIR/src est manquant"
  exit 1
fi

pushd "$WS_DIR" >/dev/null

rosdep update
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash

exec ros2 launch wall_e_bringup bringup.launch.py
