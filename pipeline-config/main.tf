locals {
  raw_requests = jsondecode(
    file("requests.json")
  )
  # Turn it into a map so we can for_each by bucket_name or index
  requests = {
    for idx, r in local.raw_requests :
    idx => r
  }
}

data "aws_caller_identity" "current" {}

resource "aws_s3_bucket_policy" "read_only_policy" {
  # count  = var.is_access_request ? 1 : 0   #check if the flag is_access_request is set to true or false. if set to false destroy the corresponding access
  for_each = {
    for key, req in local.requests :
    key => req
    if req.is_access_request
  }
  bucket = each.value.bucket_name

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/aws-reserved/sso.amazonaws.com/${var.principal_arn}"
        }
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ],
        Resource = [
          "arn:aws:s3:::${var.bucket_name}",
          "arn:aws:s3:::${var.bucket_name}/*"
        ]
      }
    ]
  })
}