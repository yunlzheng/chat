pipeline {
  agent any
  stages {
    stage('test') {
      parallel {
        stage('test') {
          steps {
            readYaml(file: 'containerization-spring-with-helm/charts/values.yaml')
            writeYaml(file: 'containerization-spring-with-helm/charts/values.yaml', data: 'a')
          }
        }
        stage('test2') {
          steps {
            sh 'echo hello'
          }
        }
      }
    }
  }
}