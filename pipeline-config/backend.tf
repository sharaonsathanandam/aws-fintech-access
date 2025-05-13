terraform {
  backend "s3" {
    bucket         = "fintech-access-tfstate-bucket"
    key            = "env/dev/terraform.tfstate"
    region         = "us-east-2"
    encrypt        = true
    dynamodb_table = "access-terraform-locks"
  }
}