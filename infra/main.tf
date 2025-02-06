# ---------------------------------------------
# ---- Instantiate Terraform w/ S3 backend ----
# ---------------------------------------------

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      # version = "~> 4.0"
    }
  }
  backend "s3" {
    key    = "terraform.tfstate"
  }

}

# ---------------------------------------------
# ---- Specify provider (region + profile) ----
# ---------------------------------------------

provider "aws" {
  region  = var.aws_region
  profile = var.aws_profile
}

# -------------------------
# ---- Local variables ----
# -------------------------

locals {
    a_local_file_path      = "example.zip"
}