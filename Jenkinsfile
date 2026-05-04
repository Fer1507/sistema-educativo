pipeline {
    agent any

    options {
        timeout(time: 15, unit: 'MINUTES')
        disableConcurrentBuilds()
    }

    environment {
        APP_NAME   = "SistemaEducativo"
        RECIPIENT  = "admin@empresa.com"
        PYTHON_HOME = "C:\\Users\\Sergio\\AppData\\Local\\Python\\pythoncore-3.14-64"
        PATH        = "C:\\Users\\Sergio\\AppData\\Local\\Python\\pythoncore-3.14-64;C:\\Users\\Sergio\\AppData\\Local\\Python\\pythoncore-3.14-64\\Scripts;${env.PATH}"
    }

    stages {

        stage('Clonar Repositorio') {
            steps {
                echo "Descargando código del proyecto ${APP_NAME} desde GitHub..."
                git branch: 'main',
                    credentialsId: 'github-credentials',
                    url: 'https://github.com/Fer1507/sistema-educativo.git'
            }
        }

        stage('Instalar Dependencias') {
            steps {
                echo 'Instalando dependencias del proyecto...'
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Pruebas Automatizadas') {
            steps {
                echo 'Ejecutando pruebas unitarias...'
                bat 'python -m unittest discover -s tests -v'
            }
        }

        stage('Construcción') {
            steps {
                echo 'Construyendo artefactos de la aplicación...'
                bat '''
                    if not exist C:\\SistemaEducativo mkdir C:\\SistemaEducativo
                    xcopy /E /I /Y src C:\\SistemaEducativo\\src
                    echo Build completado: %DATE% %TIME% > C:\\SistemaEducativo\\build-info.txt
                '''
            }
        }

        stage('Despliegue') {
            steps {
                echo 'Desplegando aplicación en servidor local...'
                bat '''
                    echo Deteniendo servicio anterior (si existe)...
                    taskkill /F /FI "IMAGENAME eq python.exe" 2>nul || echo Sin proceso previo
                    echo Iniciando nueva version...
                    if not exist C:\\SistemaEducativo\\logs mkdir C:\\SistemaEducativo\\logs
                    start /B python C:\\SistemaEducativo\\src\\app.py 1>C:\\SistemaEducativo\\logs\\app.log 2>&1
                    echo Despliegue completado.
                '''
            }
        }

    }

    post {
        success {
            echo 'Pipeline ejecutado correctamente.'
            emailext(
                to: "${RECIPIENT}",
                subject: "[${APP_NAME}] Pipeline exitoso - Build #${BUILD_NUMBER}",
                body: """
                    <h3>El pipeline se ejecuto correctamente.</h3>
                    <p><b>Proyecto:</b> ${APP_NAME}</p>
                    <p><b>Build:</b> #${BUILD_NUMBER}</p>
                    <p><b>Rama:</b> ${GIT_BRANCH}</p>
                    <p><b>Duracion:</b> ${currentBuild.durationString}</p>
                    <p>Ver detalles: <a href="${BUILD_URL}">${BUILD_URL}</a></p>
                """,
                mimeType: 'text/html'
            )
        }
        failure {
            echo 'Se produjo un error en el pipeline.'
            emailext(
                to: "${RECIPIENT}",
                subject: "[${APP_NAME}] Pipeline fallido - Build #${BUILD_NUMBER}",
                body: """
                    <h3>El pipeline ha fallado.</h3>
                    <p><b>Proyecto:</b> ${APP_NAME}</p>
                    <p><b>Build:</b> #${BUILD_NUMBER}</p>
                    <p><b>Rama:</b> ${GIT_BRANCH}</p>
                    <p>Revise los logs: <a href="${BUILD_URL}console">${BUILD_URL}console</a></p>
                """,
                mimeType: 'text/html'
            )
        }
        always {
            echo 'Pipeline finalizado.'
        }
    }
}
