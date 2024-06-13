# Gateway Service

Este repositorio contiene el código fuente y los archivos necesarios para desplegar y ejecutar un servicio de gateway en un clúster de Kubernetes.

## Descripción

El servicio de gateway actúa como punto de entrada para la comunicación entre clientes externos y los servicios internos dentro del clúster de Kubernetes. Proporciona una interfaz unificada y segura para acceder a los diferentes microservicios que componen la aplicación.

## Proceso de Despliegue

Para desplegar el servicio de gateway en un clúster de Kubernetes, sigue los siguientes pasos:

1. **Configuración de Variables de Entorno:** Define las siguientes variables de entorno en tu flujo de trabajo de GitHub Actions o en tu entorno local:
   - `DOCKER_USERNAME`: Nombre de usuario de Docker Hub.
   - `DOCKER_PASSWORD`: Contraseña de Docker Hub.
   - `K8_NAMESPACE`: Nombre del namespace de Kubernetes donde se desplegará el servicio.
   - `K8_DEPLOYMENT`: Nombre del deployment de Kubernetes.
   - `HPA_NAME`: Nombre del HPA (Horizontal Pod Autoscaler).
   - `SERVICE_NAME`: Nombre del servicio de Kubernetes.
   - `K8_APP`: Nombre de la aplicación.

2. **Ejecución del Flujo de Trabajo:** Ejecuta el flujo de trabajo de GitHub Actions `deploy.yml`. Este flujo de trabajo construirá la imagen del contenedor, la subirá a Docker Hub y luego aplicará los recursos de Kubernetes necesarios en el clúster.

3. **Verificación del Despliegue:** Una vez completado el flujo de trabajo, verifica que el servicio de gateway esté desplegado correctamente en tu clúster de Kubernetes.

## Uso del Gateway

El servicio de gateway expone un conjunto de endpoints que permiten a los clientes externos comunicarse con los diferentes servicios dentro del clúster. Para utilizar el gateway, los clientes deben enviar solicitudes HTTP a los endpoints proporcionados por el gateway, siguiendo la especificación de la API correspondiente.

## Versiones Disponibles

- **latest:** Última versión estable del servicio de gateway. Se recomienda su uso para entornos de producción.
- **v1.0:** Versión inicial del servicio de gateway. Úsala si necesitas una versión específica del servicio que pueda tener características o comportamientos diferentes.

Para cambiar la versión del servicio de gateway, modifica la etiqueta de imagen del contenedor en el archivo `deploy.yml` antes de ejecutar el flujo de trabajo.

## Contribución

Si deseas contribuir a este proyecto, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama para tu contribución (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commits (`git commit -am 'Agrega nueva funcionalidad'`).
4. Sube tus cambios a tu repositorio remoto (`git push origin feature/nueva-funcionalidad`).
5. Crea un nuevo pull request en GitHub.

Esperamos tus contribuciones!
