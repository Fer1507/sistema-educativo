pipeline {
    agent any

    options {
        timeout(time: 15, unit: 'MINUTES')
        disableConcurrentBuilds()
    }

    environment {
        APP_NAME  = "SistemaEducativo"
        RECIPIENT = "admin@empresa.com"
    }

    stages {

        stage('Clonar Repositorio') {
            steps {
                echo "Descargando código del proyecto ${APP_NAME} desde GitHub..."
                git branch: 'main',
                    credentialsId: 'github-credentials',
                    url: 'https://github.com/usuario/proyecto.git'
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
                    if not exist dist mkdir dist
                    xcopy /E /I /Y src dist\\src
                    echo Build completado: %DATE% %TIME% > dist\\build-info.txt
                '''
            }
        }

        stage('Despliegue') {
            steps {
                echo 'Desplegando aplicación en servidor local...'
                bat '''
                    echo Deteniendo servicio anterior (si existe)...
                    taskkill /F /IM python.exe /FI "WINDOWTITLE eq app*" 2>nul || echo Sin proceso previo
                    echo Iniciando nueva version...
                    if not exist logs mkdir logs
                    start /B python dist\\src\\app.py > logs\\app.log 2>&1
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
            echo 'Limpiando workspace...'
            cleanWs()
        }
    }
}
