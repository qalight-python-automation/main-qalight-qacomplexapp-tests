#!groovy
//
// QA Complex App tests Runner

// Pipeline
pipeline {
  agent {
    label 'master'
  }
  options {
    timeout(time: 1, unit: 'HOURS')
    timestamps()
  } // options
  stages {
    stage('\u2776 Test') {
      steps {
        script {
          currentBuild.displayName = "#${env.BUILD_NUMBER} (${env.GIT_COMMIT.take(8)}) ${env.GIT_BRANCH}"
          sh '''#!/usr/bin/env bash
            # Write safe shell scripts
            set -euf -o pipefail
            export
            # Install requirements
            python -m pip install -r requirements.txt
            # Run tests
            python -m pytest -n 5
            # EOF
          '''
        } // script
      } // steps
    } // stage
  } // stages
  post {
    always {
      cleanWs()
    } // always
  } // post
} // pipeline

// vim: ft=groovy
// EOF
