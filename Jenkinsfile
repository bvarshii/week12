pipeline {
    agent any

    stages {

        stage('Run Selenium Tests with pytest') {
            steps {
                echo "🚀 Running Selenium Tests using pytest"

                // Install Python dependencies
                bat 'python -m pip install --upgrade pip'
                bat 'python -m pip install -r requirements.txt'

                // ✅ Start Flask app in background
                bat 'start /B python app.py'

                // 🕒 Wait until Flask is up (retry until reachable)
                bat '''
                powershell -Command "
                for ($i=0; $i -lt 15; $i++) {
                    try {
                        $res = (Invoke-WebRequest http://127.0.0.1:5000 -UseBasicParsing).StatusCode
                        if ($res -eq 200) { Write-Host 'Flask is ready ✅'; exit 0 }
                    } catch {
                        Start-Sleep -Seconds 2
                    }
                }
                Write-Error '❌ Flask did not start in time'; exit 1
                "
                '''

                // ✅ Run Selenium tests (headless mode to avoid GUI requirement)
                bat 'pytest -v --maxfail=1 --disable-warnings --tb=short'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🐳 Building Docker Image"
                bat "docker build -t seleniumdemoapp:v1 ."
            }
        }

        stage('Docker Login') {
            steps {
                // ⚠️ Use Jenkins credentials instead of plain text password
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat 'docker login -u %DOCKER_USER% -p %DOCKER_PASS%'
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                echo "📤 Pushing Docker Image to Docker Hub"
                bat "docker tag seleniumdemoapp:v1 bvarshii/sample:seleniumtestimage"
                bat "docker push bvarshii/sample:seleniumtestimage"
            }
        }

        stage('Deploy to Kubernetes') { 
            steps { 
                echo "🚢 Deploying to Kubernetes"
                bat 'kubectl apply -f deployment.yaml --validate=false'
                bat 'kubectl apply -f service.yaml'
            } 
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Please check the logs.'
        }
    }
}
