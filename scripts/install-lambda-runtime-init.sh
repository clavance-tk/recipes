#!/bin/bash
# NOTE: this should cause this log to happen when calling a lambda, in future versions of localstack might change "Installation of lambda-runtime skipped (already installed)."
# Using lambda-runtime because we are using version 2.3.2 of localstack if you are using an older version the folder is awslambda-runtime
folder=./volume/lib/lambda-runtime/travelperk-fix-macos-virtiofs/arm64/var/rapid
is_macos=$(uname -a | grep Darwin)
if [[ $is_macos ]] ; then
  if [[ -d $folder ]] ; then
    mkdir -p $folder
  fi
  if ! shasum -c aws-lambda-rie-arm64.checksum ; then
    echo "Checksum failed, downloading the patched version"
    # installing custom aws-lambda-rie-arm64
    export AWS_PROFILE=tooling
    # this version comes from https://github.com/localstack/lambda-runtime-init/pull/28/files
    # We compiled this using `ARCH=arm64` with `make compile-with-docker`, then uploaded `bin/aws-lambda-rie-arm64` to our S3 bucket
    # by the way, this is using latest version (not v0.1.19-pre) but it seems to work without any problem with localstack 2.2
    aws s3 cp s3://tk-tooling-engineering-operations/localstack-lambda-runtime-init/aws-lambda-rie-arm64 ${folder}/init
    chmod +x ${folder}/init
  else
    echo "Checksum passed, patched version already available"
  fi
else
  echo "Not MacOS, skipping the custom aws-lambda-rie-arm64"
fi
