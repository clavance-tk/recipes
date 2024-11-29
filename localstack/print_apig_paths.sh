#!/bin/bash
# This command will print out the API Gateway paths and handlers for the given API Gateway ID from the pulumilocal stack
# There is also a second base url that you can use directly with cURL to the test the endpoints are responding as expected
# Usage: ./print_apig_paths.sh will print these values from the first API gateway is running in local stack
# Output: GET http://PetsApiGateway.execute-api.localhost.localstack.cloud:4566/dev/hello -> src/api/handler.hello_handler

api_info=$(awslocal apigateway get-rest-apis)
api_id=$(echo "$api_info" | grep -o '"id": "[^"]*' | sed 's/"id": "//')

base_url="http://$api_id.execute-api.$AWS_DEFAULT_REGION.amazonaws.com/test"
curl_base_url="http://localhost:4000/restapis/$api_id/test/_user_request_"

# Get the paths and handlers from the API Gateway
urls_and_handlers=$(awslocal apigateway get-resources\
  --rest-api-id $api_id\
  --query "items[?resourceMethods].{path: path, func: resourceMethods.[*][].{method: httpMethod, lambdaUri: methodIntegration.uri}} | [].[func[0].method, path, func[0].lambdaUri]"\
  --output text
)

urls=""
example_curl_get_url=""
while read -r line; do
  method=$(echo "$line" | awk '{print $1}')
  path=$(echo "$line" | awk '{print $2}')

  if [ "$method" = "GET" ]; then
    example_curl_get_url="$curl_base_url$path"
  fi

  lambdaUri=$(echo "$line" | awk '{print $3}')
  lambdaArn=$(echo "$lambdaUri" | sed -E 's/.*arn:aws:lambda:([^:]+):([^:]+):function:([^:]+).*/\3/')

  # Retrieve the handler from the Lambda function
  handler=$(awslocal lambda get-function --function-name "$lambdaArn" --query "Configuration.Handler" --output text)

  urls="${urls}\n${method} ${base_url}${path} -> ${handler}"
done <<< "$urls_and_handlers"

echo "------ Generated Endpoints ------"
echo -e "$urls" | sort
echo "---------------------------------"
echo "------- cURL Endpoint -----"
echo "You can request any of the paths above via cURL, using the following base address:"
echo "$curl_base_url"
if [ -n "$example_curl_get_url" ]; then
  echo "GET example: curl $example_curl_get_url"
fi
echo "---------------------------------"
