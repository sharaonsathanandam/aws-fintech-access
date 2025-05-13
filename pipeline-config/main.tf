resource "aws_s3_bucket_policy" "read_only_policy" {
  count = var.is_access_request ? 1 : 0
  bucket = var.bucket_name
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          AWS = "arn:aws:iam::632234552152:role/aws-reserved/sso.amazonaws.com/${var.principal_arn}"
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