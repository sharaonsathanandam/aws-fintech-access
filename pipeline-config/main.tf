locals {
  raw_requests = jsondecode(
    file("requests.json")
  )
  bucket_names = distinct([ for r in local.raw_requests : r.bucket_name ])

  # group each request under its bucket
  requests_by_bucket = {
    for b in local.bucket_names :
    b => [
      for r in local.raw_requests :
      r if r.bucket_name == b && r.is_access_request
    ]
  }
}

data "aws_caller_identity" "current" {}

resource "aws_s3_bucket_policy" "read_only_policy" {
  # count  = var.is_access_request ? 1 : 0   #check if the flag is_access_request is set to true or false. if set to false destroy the corresponding access
  for_each = local.requests_by_bucket
  bucket = each.key

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect    = "Allow"
        Principal = {
          AWS = distinct([
            for req in each.value :
            "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/aws-reserved/sso.amazonaws.com/${req.principal_arn}"
          ])
        }
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ],
        Resource = [
          "arn:aws:s3:::${each.key}",
          "arn:aws:s3:::${each.key}/*"
        ]
      }
    ]
  })
}