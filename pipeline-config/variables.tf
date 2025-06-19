variable "force_destroy" {
  description = "Force delete even if objects exist"
  type        = bool
  default     = false
}

variable "is_access_request" {
  type = bool
  default = true
}