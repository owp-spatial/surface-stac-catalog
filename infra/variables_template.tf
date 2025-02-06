# -------------------------------------------------------------------------------
# ---- UNCOMMENT THIS FILE TO USE this file as a VARIABLES TEMPLATE ----
# ---- These are the variables that are used in this Terraform configuration ----
# -------------------------------------------------------------------------------

# # AWS account number to use for AWS CLI.
variable "aws_account_number" {
  description = "Account number."
  type        = string
  sensitive   = true
}

# AWS profile to use for AWS CLI.
variable "aws_profile" {
  description = "Profile to use for AWS CLI."
  type        = string
}

# AWS region to use for AWS CLI.
variable "aws_region" {
  description = "Region to use for AWS CLI."
  type        = string
}