terraform {
  required_providers {
    aws = {
        source = "hashicorp/aws"
        version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "mv-tf-state1"
    key    = "value"
    region = "eu-west-1"
    encrypt = true
    dynamodb_table = "tf-strava-ingestion"
  }
}

provider "aws" {
  region = "eu-west-1"
}

locals {
  project = "strava-ingestion"
}


resource "aws_sns_topic" "topic" {
  name = "strava-updates"

  tags = {
    Project = local.project
  }
  
}