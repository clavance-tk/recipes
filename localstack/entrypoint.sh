#!/bin/bash
set -e

# This entrypoint is used to fix the file watcher issue on MacOS

uname -a | grep aarch64 && is_arm64=true || is_arm64=false

if [[ $is_arm64 == true ]] ; then
    echo "Running on arm64, assuming macOS"
    export LAMBDA_INIT_RELEASE_VERSION="travelperk-fix-macos-virtiofs"
fi

docker-entrypoint.sh $@
