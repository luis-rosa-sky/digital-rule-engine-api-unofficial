#!/bin/bash

ENVIRONMENT="${1:-dev}"

# delete temp folders older than one day
find /tmp/eudr-webappmain-* -type d -ctime +1 | xargs rm -rf

# set working dir
cd $(dirname "${BASH_SOURCE[0]}")
echo "Working directory: ${PWD}"
echo "Environment: ${ENVIRONMENT}"
echo "Service: eudr-webappmain"
echo "Namespace: eudr"

# set config dir
# ssm runs as root, not ssm-user
export KUBECONFIG=/root/.kube/config

# ensure namespace is present
kubectl get namespace "eudr" || kubectl create namespace "eudr"

# deploy and wait
kubectl apply -n "eudr" -f "chart/components-${ENVIRONMENT}.yaml"
kubectl rollout status deploy -n "eudr" "eudr-webappmain"