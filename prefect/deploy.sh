#!/bin/bash
# ELT deployment script in S3
cd /tmp
mkdir -p deployment/flows
cp -r /root/prefect/flows/*.py deployment/flows
cp -r /root/dbt deployment/
cp -r /root/great_expectations deployment
cd deployment
# you can create a deploy file with:
# prefect deployment build flows/elt_flow.py:elt_flow -n elt -q default -sb remote-file-system/dev
cp /root/prefect/elt_flow-deployment.yaml .
touch .prefectignore
prefect deployment apply elt_flow-deployment.yaml --upload