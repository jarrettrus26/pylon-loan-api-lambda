version = 0.1
[default]
[default.deploy]
[default.deploy.parameters]
stack_name = "pylon-loan-stack"
s3_bucket = "aws-sam-cli-managed-default-samclisourcebucket-10lyk50w37ylg"
s3_prefix = "pylon-loan-stack"
region = "us-west-1"
confirm_changeset = true
capabilities = "CAPABILITY_IAM"
disable_rollback = true
image_repositories = []
