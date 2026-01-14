pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
        RESULTS_DIR = "results"
    }

    stages {
        stage('Checkout') {
            steps {
                // Récupère ton code depuis Git
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                script {
                    // Crée un virtualenv et installe les dépendances
                    if (isUnix()) {
                        sh """
                        python3 -m venv ${VENV_DIR}
                        source ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                        """
                    } else {
                        bat """
                        python -m venv ${VENV_DIR}
                        call ${VENV_DIR}\\Scripts\\activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                        """
                    }
                }
            }
        }

        stage('Run Robot Tests') {
            steps {
                script {
                    if (isUnix()) {
                        sh """
                        source ${VENV_DIR}/bin/activate
                        mkdir -p ${RESULTS_DIR}
                        robot --outputdir ${RESULTS_DIR} tests/
                        """
                    } else {
                        bat """
                        call ${VENV_DIR}\\Scripts\\activate
                        if not exist ${RESULTS_DIR} mkdir ${RESULTS_DIR}
                        robot --outputdir ${RESULTS_DIR} tests
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            // Publie les rapports Robot Framework
            robot outputPath: "${RESULTS_DIR}",
                  outputFileName: "output.xml",
                  reportFileName: "report.html",
                  logFileName: "log.html"
        }

        success {
            echo "✅ All Robot Framework tests passed!"
        }

        failure {
            echo "❌ Some tests failed! Check the report."
        }
    }
}
