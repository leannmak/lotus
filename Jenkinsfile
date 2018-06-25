#!/usr/bin/env groovy Jenkinsfile

pipeline {
    agent {
        node {
            label 'master'
            customWorkspace 'workspace/lotus'
        }
    }
    triggers {
        pollSCM('* * * * *')
    }
    stages {
        stage('env init') {
            steps {
                sh '''
                    source ~/.bash_profile>/dev/null 2>&1
                    if [ -n "`pyenv versions | grep lotus`" ]; then pyenv virtualenv-delete -f lotus; fi
                    pyenv virtualenv system lotus
                '''
            }
        }
        stage('pull package') {
            steps {
                sh '''
                    if [ -n "`ls | grep lotus`" ]; then rm -rf lotus; fi
                    git clone https://github.com/leannmak/lotus.git
                '''
            }
        }
        stage('test') {
            steps {
                sh '''
                    source ~/.bash_profile>/dev/null 2>&1
                    pyenv activate lotus
                    pip install --upgrade pip
                    pip install tox
                    cd lotus
                    tox
                '''
            }
        }
        stage('dependencies install') {
            steps {
                sh '''
                    source ~/.bash_profile>/dev/null 2>&1
                    pyenv activate lotus
                    cd lotus
                    pip install -r requirements.txt
                '''
            }
        }
        stage('build') {
            steps {
                sh '''
                    source ~/.bash_profile>/dev/null 2>&1
                    pyenv activate lotus
                    cd lotus
                    python setup.py clean --all >/dev/null
                    python setup.py install
                    python -c "import lotus"
                '''
            }
        }
    }
    post {
        always {
            junit 'lotus/nosetests.xml'
            step([
                $class: 'CoberturaPublisher', autoUpdateHealth: false,
                autoUpdateStability: false, coberturaReportFile: 'lotus/coverage.xml',
                failUnhealthy: false, failUnstable: false, maxNumberOfBuilds: 0,
                onlyStable: false, sourceEncoding: 'ASCII', zoomCoverageChart: false])
            cleanWs()
        }
        success {
            sh '''
                source ~/.bash_profile>/dev/null 2>&1
                pyenv virtualenv-delete -f lotus
            '''
        }
        failure {
            emailext body: '$DEFAULT_CONTENT', subject: '$DEFAULT_SUBJECT', to: 'leannmak@139.com'
        }
    }
}
