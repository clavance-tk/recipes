#!/bin/bash
set -e

# This script should be used to locally bring up this project's pulumi stack for local testing

# Temporarily set the stacks passphrase to empty string for ease of testing
export PULUMI_CONFIG_PASSPHRASE=""
export PULUMI_SKIP_UPDATE_CHECK=true
export PULUMI_BACKEND_URL='s3://localstack-pulumi-states?endpoint=localhost:4566&region=us-east-2&disableSSL=true&s3ForcePathStyle=true'
export AWS_DEFAULT_REGION=us-east-1
export AWS_REGION=us-east-1
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test

PATH_TO_THIS_PROJECTS_ROOT="$(git rev-parse --show-toplevel)"
PATH_TO_THIS_PROJECTS_INFRA="$PATH_TO_THIS_PROJECTS_ROOT/infra/envs"
STACK_NAME="local"
STACK_PATH="organization/recipes/$STACK_NAME"
STACK_DEPENDENCY_DATA_PATH="$PATH_TO_THIS_PROJECTS_ROOT/localstack/config/stack_dependency_data"

pulumi_up_this_projects_stack() {
    echo "Initiating this project's local stack"
    pulumilocal stack init $STACK_PATH --cwd $PATH_TO_THIS_PROJECTS_INFRA
    rm -r "$PATH_TO_THIS_PROJECTS_INFRA/Pulumi.$STACK_NAME.yaml" # A pulumi file is created in root that we do not need

    # In order to give the correct config in CircleCi or local we must use a temp file copied from the current dir

    yaml_config="$PATH_TO_THIS_PROJECTS_ROOT/localstack/config/pulumi-$STACK_NAME.yaml"

    config_temp_file="$(mktemp).yaml"
    cp -v "${yaml_config}" "${config_temp_file}"

    pulumilocal --non-interactive up \
        -s "$STACK_PATH" \
        --config-file "$config_temp_file" \
        --cwd "$PATH_TO_THIS_PROJECTS_INFRA" --yes \
        --config core:src_project_path="$PATH_TO_THIS_PROJECTS_ROOT" \
        --config recipes:test_hot_reload_code_path="$HOT_RELOAD_PATH"

    # Remove the file automatically created by pulumi on up
    rm "$PATH_TO_THIS_PROJECTS_INFRA/Pulumi.local.yaml"
}

# ---- Start of Script execution -----
echo "Creating localstack S3 buckets to hold files needed for provisioning"
awslocal s3 mb s3://localstack-pulumi-states
awslocal s3 mb s3://tk-test-lambda-bundles
awslocal s3 mb s3://tk-test-okta-data

echo "Copying files from tooling and local to the s3 local stack buckets"
aws s3 --profile=tooling cp s3://tk-tooling-pulumi-state/exports/tk-core-deps/local.json "$STACK_DEPENDENCY_DATA_PATH/core-deps-state-local.json"
awslocal s3 cp "$STACK_DEPENDENCY_DATA_PATH/squads.yaml" s3://tk-test-okta-data/squads.yaml

echo "Initiating and importing the tk-core-deps local stack so it can be referenced by project"
pulumilocal stack init organization/tk-core-deps/local --cwd $STACK_DEPENDENCY_DATA_PATH
pulumilocal stack import -s organization/tk-core-deps/local --file $STACK_DEPENDENCY_DATA_PATH/core-deps-state-local.json --cwd $STACK_DEPENDENCY_DATA_PATH

echo "Deleting temporary core deps files now that the stacks is up"
rm "$STACK_DEPENDENCY_DATA_PATH/core-deps-state-local.json"
rm "$STACK_DEPENDENCY_DATA_PATH/Pulumi.local.yaml"

pulumi_up_this_projects_stack


