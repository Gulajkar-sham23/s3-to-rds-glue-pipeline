pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/<username>/s3-to-rds-glue-pipeline.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t s3-to-rds-glue .'
            }
        }

        stage('Push to ECR') {
            steps {
                sh '''
                aws ecr get-login-password --region <REGION> | docker login --username AWS --password-stdin <ECR_REPOSITORY_URL>
                docker tag s3-to-rds-glue:latest <ECR_REPOSITORY_URL>/s3-to-rds-glue:latest
                docker push <ECR_REPOSITORY_URL>/s3-to-rds-glue:latest
                '''
            }
        }

        stage('Deploy Terraform Resources') {
            steps {
                sh '''
                cd terraform
                terraform init
                terraform apply -auto-approve
                '''
            }
        }
    }
}
