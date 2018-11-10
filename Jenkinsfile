pipeline {
    agent {
        dockerfile {
            filename 'jenkins/Dockerfile.agent'
            args '-v /var/run/docker.sock:/var/run/docker.sock --network unibrowser-test-net'
        }
    }
    environment {
        SCRAPER_IMAGE = 'unibrowser/unibrowser-scraper'
        SCRAPER_NAME = 'unibrowser-scraper'
        BRIDGE_NET = 'unibrowser-net'
    }
    stages {
        stage('Install Dependencies'){
            steps {
                sh './jenkins/install-depend.sh'
            }
        }
        stage('Test') {
            steps {
                sh 'pytest || true'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker build . -t $SCRAPER_IMAGE'
                sh 'docker rm -f $SCRAPER_NAME || true'
                sh 'docker run -d --name $SCRAPER_NAME --restart always --network $BRIDGE_NET $SCRAPER_IMAGE'
            }
        }
    }
}