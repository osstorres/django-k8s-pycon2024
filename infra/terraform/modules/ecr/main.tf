resource "aws_ecr_repository" "repositories" {
  count = length(var.repository_names)

  name = var.repository_names[count.index]

  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = var.repository_names[count.index]
  }
}