#!/bin/bash
set -e

# Enter docker app folder
cd /app

uname -a | grep aarch64 && is_arm64=true || is_arm64=false

if [[ $is_arm64 == true ]] ; then
  echo "Running on arm64, assuming macOS"
  echo "checking we have the patched version of aws-lambda-rie-arm64"
  echo "if this fails please run \`make setup-lambda-runtime-init\`"
  shasum -c aws-lambda-rie-arm64.checksum || exit 1  # verify we have the patched version
else
  echo "Not arm64, skipping the custom aws-lambda-rie-arm64"
fi

set -xe

# Install Pulumi dependencies needed to locally test
export PATH=$PATH:/root/.pulumi/bin
pulumi_version=$(pulumi version | sed 's/^v//')
pulumi_latest_version=$(curl -s https://www.pulumi.com/latest-version)
if [[ $pulumi_version != $pulumi_latest_version ]]; then
  echo "Pulumi version $pulumi_version is not the latest version available, installing $pulumi_latest_version"
  curl -fsSL https://get.pulumi.com | sh
  export PATH=$PATH:/root/.pulumi/bin
fi

# Only install the python pulumi dependencies needed to bring up the pulumi local stack
pip install -r localstack/requirements-pulumi-local.txt

/app/scripts/pulumi-up-localstack.sh

/app/localstack/print_apig_paths.sh
