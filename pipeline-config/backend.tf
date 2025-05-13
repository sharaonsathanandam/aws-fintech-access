terraform {
  backend "s3" {
    bucket         = "fintech-s3-tfstate-bucket"
    key            = "env/dev/terraform.tfstate"
    region         = "us-east-2"
    encrypt        = true
    dynamodb_table = "s3-terraform-locks"
  }
}