def allYamls = []
def delYamls = []
pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = 'us-east-2'
        AWS_ACCESS_KEY_ID     = credentials('Terraform-CICD')
        AWS_SECRET_ACCESS_KEY = credentials('Terraform-CICD')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Apply Access Request') {
            steps{
                script{
                    sh "python3 scripts/parse_yaml.py"
                    def tfvarsFile = "pipeline-config/requests.json"
                    sh "cat ${tfvarsFile}"
                    dir('pipeline-config') {
                          sh "cat requests.json"
                          sh '/usr/local/bin/terraform init -reconfigure'
                          sh '/usr/local/bin/terraform plan -refresh=false -out=tfplan'
                          input message: "Apply changes for access request?", ok: "Apply Now"
                          sh '/usr/local/bin/terraform apply -refresh=false -auto-approve tfplan'
                        }
                    }
                }
            }
        }
    }