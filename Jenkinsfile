pipeline {
    agent {
        dockerfile {
            filename 'jenkins/Dockerfile.agent'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    environment {
        SCRAPER_IMAGE = 'unibrowser/unibrowser-scraper'
        SCRAPER_NAME = 'unibrowser-scraper'
    }
    stages {
        stage('Install Dependencies'){
            steps {
                sh './jenkins/install-depend.sh'
            }
        }
        stage('Test') {
            steps {
                sh 'pytest'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker build . -t $SCRAPER_IMAGE'
                sh 'docker rm -f $SCRAPER_NAME || true'
                sh 'docker run -d --name $SCRAPER_NAME --restart always $SCRAPER_IMAGE'
            }
        }
    }
}