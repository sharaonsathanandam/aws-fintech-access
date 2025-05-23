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

        stage('Get YAML Commit Hashes') {
            steps {
                script {
                    // Step 1: Get recently changed and added files
                    def changedFiles = sh(script: 'git diff --name-only --diff-filter=M HEAD~1 HEAD', returnStdout: true).trim().split('\n')
                    def newFiles = sh(script: 'git diff --name-only --diff-filter=A HEAD~1 HEAD', returnStdout: true).trim().split('\n')
                    def deletedFiles = sh(script: 'git diff --name-only --diff-filter=D HEAD~1 HEAD', returnStdout: true).trim().split('\n')

                    // Step 2: Filter YAML files from each list
                    def changedYamls = changedFiles.findAll { it.endsWith(".yaml") }
                    def newYamls = newFiles.findAll { it.endsWith(".yaml") }
                    delYamls = deletedFiles.findAll { it.endsWith(".yaml") }

                    echo "Changed YAML files: ${changedYamls}"
                    echo "New YAML files: ${newYamls}"
                    echo "Deleted YAML files: ${delYamls}"

                    // Step 3: Combine and deduplicate
                    allYamls = (changedYamls + newYamls).unique()

                    if (allYamls.isEmpty()) {
                        echo "No new or updated YAMLs found. Skipping pipeline."
                        currentBuild.result = 'SUCCESS'
                        return
                      }

                    // Step 4: Get commit hash for each file
                    allYamls.each { file ->
                        def commitHash = sh(
                            script: "git log -n 1 --pretty=format:%H -- ${file}",
                            returnStdout: true
                        ).trim()
                        echo "${file} was last modified in commit ${commitHash}"
                    }
                }
            }
        }

        stage('Process New YAMLs') {
            steps{
                script{
                    echo "All changed files inside next stage: ${allYamls}"
                    for (yamlFile in allYamls) {
                        if (!fileExists(yamlFile)) {
                            echo "Skipping ${yamlFile} — it was deleted in this commit."
                            continue
                          }
                        def commitHash = sh(script: "git log -n 1 --pretty=format:%H -- ${yamlFile}", returnStdout: true).trim()
                        echo "Processing ${yamlFile} (commit ${commitHash})"
                        sh "python3 -m pip install -r scripts/requirements.txt"
                        sh "python3 scripts/parse_yaml.py ${yamlFile}"

                        def tfvarsFile = "pipeline-config/terraform.tfvars.json"
//                         sh "jq '. + {git_commit_hash: \"${commitHash}\"}' ${tfvarsFile} > tmp && mv tmp ${tfvarsFile}"
                        sh "cat ${tfvarsFile}"
                        dir('pipeline-config') {
                          sh '/usr/local/bin/terraform init -reconfigure'
                          sh '/usr/local/bin/terraform plan -refresh=false -out=tfplan'
                          input message: "Apply changes for ${yamlFile}?", ok: "Apply Now"
                          sh '/usr/local/bin/terraform apply -auto-approve tfplan'
                        }
                    }
                }
            }
        }
        stage('Revoke Deleted Access') {
          steps {
            script {
              for (yamlFile in delYamls) {
                echo "Revoking access from deleted file: ${yamlFile}"
                sh "python3 scripts/revoke_access.py ${yamlFile}"
                def tfvarsFile = "pipeline-config/terraform.tfvars.json"
                sh "cat ${tfvarsFile}"
                dir('pipeline-config') {
                  sh '/usr/local/bin/terraform init -reconfigure'
                  sh '/usr/local/bin/terraform plan -refresh=false -out=tfplan'
                  input message: "Apply changes for ${yamlFile}?", ok: "Apply Now"
                  sh '/usr/local/bin/terraform apply -auto-approve tfplan'
                }
           }
        }
      }
    }
 }
}