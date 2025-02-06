# -----------------------------------------------
# S3 bucket for storing the Terraform state files
# -----------------------------------------------

data "aws_s3_bucket" "terraform_state_s3_bucket" {
  bucket = var.tfstate_s3_bucket_name
}

# -----------------------------------------------
# S3 bucket for storing the Surface STAC Catalog 
# -----------------------------------------------


