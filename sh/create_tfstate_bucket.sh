#!/bin/bash
# ----- NEW VERSION THAT DOES NOT USE AWS PROFILE AS AN ARGUMENT -----
# Create a ECR repository for use by the infrastructure created by Terraform (e.g. Docker images). 
# This script is run before terraform plan/apply to ensure that certain stack resources (ECR repository, S3 buckets, etc)
#  exist before terraform tries to use the Docker Image while creating infrastructure (e.g. Lambda functions in this case)


# Provide following as arguments to script: 
# 1. AWS Account Number (e.g. 123456789)
# 2. AWS region (e.g. "us-east-1")
# 3. Terraform state S3 bucket name to create (if it does not exist, e.g. "tfstate-s3-bucket-name")
# 4. RUNNING_ON_GITHUB_ACTION ("true" or "false") - Optional, default is "false"

# Example: source sh/create_tfstate_bucket.sh 123456789 aws-region tfstate-s3-bucket-name "false"

# AWS Account Number
AWS_ACCOUNT_NUMBER=$1

# AWS Region to create/check resources, if not given, use "us-east-1"
AWS_REGION=${2:-"us-east-1"}
LOCATION_CONSTRAINT=${AWS_REGION}

# Terraform state S3 bucket name
TF_STATE_S3_BUCKET_NAME=$3

# Flag to determine whether to export variables to $GITHUB_ENV
RUNNING_ON_GITHUB_ACTION=${4:-"false"}

echo "- AWS_REGION: $AWS_REGION"
echo "- TF_STATE_S3_BUCKET_NAME: $TF_STATE_S3_BUCKET_NAME"
echo "- LOCATION_CONSTRAINT: $LOCATION_CONSTRAINT"

# -----------------------------------------------------------------------------------------------
# ----- Create S3 bucket to keep Terraform state files (if does NOT exist) -----
# -----------------------------------------------------------------------------------------------

# check if Terraform state S3 bucket ALREADY EXISTS
if ! aws s3api head-bucket --bucket "$TF_STATE_S3_BUCKET_NAME" 2>/dev/null; then
    # Create the Terraform state S3 bucket if it DOESN'T exist
    aws s3api create-bucket --bucket "$TF_STATE_S3_BUCKET_NAME" \
    --region "$AWS_REGION" \
    --create-bucket-configuration LocationConstraint="$LOCATION_CONSTRAINT"
    
    echo "S3 bucket $TF_STATE_S3_BUCKET_NAME created."

    # Enable versioning on the bucket
    aws s3api put-bucket-versioning --bucket "$TF_STATE_S3_BUCKET_NAME" \
    --region "$AWS_REGION" \
    --versioning-configuration Status=Enabled

else
    echo "Bucket $TF_STATE_S3_BUCKET_NAME already exists."
fi

# -----------------------------------------------------------------------------------------------
# ----- Export Terraform variables -----
# -----------------------------------------------------------------------------------------------

# Export the name of the tfstate S3 bucket as an environment variable
export TF_VAR_tfstate_s3_bucket_name="$TF_STATE_S3_BUCKET_NAME"

# Check if the script is running on GitHub Actions and the flag is set to true
if [[ "$RUNNING_ON_GITHUB_ACTION" == "true" ]]; then
    echo "Running on GitHub Actions, exporting environment variables to Github Env..."
    # Export the environment variables to $GITHUB_ENV
    echo "TF_VAR_tfstate_s3_bucket_name=$TF_STATE_S3_BUCKET_NAME" >> $GITHUB_ENV
    echo "Exported and TF_VAR_tfstate_s3_bucket_name to Github Env"
fi