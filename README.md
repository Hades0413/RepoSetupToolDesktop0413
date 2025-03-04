# Generador de Commits Automatizado v1.0

Este proyecto es una aplicación gráfica en Python que permite generar y realizar commits automatizados en un repositorio de GitHub, utilizando parámetros configurables como el número de commits por mes, el rango de meses y el año. La interfaz gráfica está construida con `tkinter`, y las variables de entorno se gestionan mediante el paquete `python-dotenv`.

Este proyecto es **Open Source**, lo que te permite colaborar, modificar y distribuir el código bajo los términos de la licencia proporcionada.

> **Aviso Importante**: Este proyecto ha sido creado con fines académicos y educativos. Su objetivo principal es facilitar la comprensión de la automatización de procesos con Git y la creación de aplicaciones gráficas. No tiene la intención de hacer mal uso de los datos o interactuar de manera no ética con los repositorios.

## Requisitos

Antes de ejecutar el proyecto, asegúrate de tener lo siguiente:

- Python 3.x instalado
- Git instalado en tu máquina
- Un token de GitHub (puedes generar uno desde [aquí](https://github.com/settings/tokens))
- Acceso al repositorio de GitHub donde deseas generar los commits

## Instalación

1. **Clona este repositorio**:

   ```bash
   git clone https://github.com/Hades0413/RepoSetupToolDesktop0413.git
   ```

   Luego, navega al directorio del proyecto:

   ```bash
   cd RepoSetupToolDesktop0413
   ```

2. **Crea un entorno virtual**:

   Es recomendable crear un entorno virtual para evitar conflictos con las dependencias del sistema.

   ```bash
   python3 -m venv prueba
   ```

   Activa el entorno virtual:

   En **Windows**:

   ```bash
   .\prueba\Scripts\activatea
   ```

   En **Linux/Mac**:

   ```bash
   source prueba/bin/activate
   ```

3. **Instala las dependencias**:

   Una vez activado el entorno virtual, instala las dependencias necesarias:

   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. **Configura las variables de entorno**:

   Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

   ```bash
   GITHUB_TOKEN=<tu_token_de_github>
   REPO_OWNER=<dueño_del_repositorio>
   REPO_NAME=<nombre_del_repositorio>
   BASE_BRANCH=<rama_base>
   USER_EMAIL=<tu_email>
   ```

   Las variables de entorno se cargan automáticamente desde el archivo `.env` para garantizar que los datos sensibles no estén hardcodeados en el código.

2. **Ejecuta la aplicación**:

   Inicia la aplicación de la siguiente manera:

   ```bash
   python create_commits.py
   ```

   Esto abrirá una interfaz gráfica donde podrás configurar el repositorio, el número de commits por mes y el rango de meses para generar los commits automáticamente.

## Estructura del Proyecto

- `commit_generator.py`: Contiene la lógica de la aplicación y la gestión de commits.
- `requirements.txt`: Archivo con las dependencias necesarias para ejecutar el proyecto.
- `.env`: (Opcional) Archivo para almacenar las variables de entorno de manera segura.
- `README.md`: Este archivo.

## Dependencias

Este proyecto utiliza las siguientes librerías:

- `tkinter`: Para la interfaz gráfica de usuario (GUI).
- `python-dotenv`: Para manejar las variables de entorno desde un archivo `.env`.
- `gitpython`: Para interactuar con el repositorio de Git.
- `datetime`: Para manejar las fechas y los tiempos de los commits.

## Contribuciones

Las contribuciones son bienvenidas. Si tienes una idea o encuentras un error, por favor abre un **issue** o envía un **pull request**.

Para contribuir, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama para tu cambio: `git checkout -b mi-nueva-funcionalidad`.
3. Haz los cambios necesarios y realiza un commit: `git commit -am 'Añadir nueva funcionalidad'`.
4. Envía los cambios a tu repositorio: `git push origin mi-nueva-funcionalidad`.
5. Crea un pull request desde tu repositorio a `main` de este proyecto.

## Seguridad

La seguridad del proyecto es una prioridad. A continuación, algunas medidas clave para asegurar el uso responsable y seguro del software:

1. **Uso de tokens seguros**: Nunca compartas tu token de GitHub públicamente. Almacénalo en un archivo `.env` y asegúrate de que esté fuera de los commits. Utiliza la librería `python-dotenv` para cargar las variables de entorno de manera segura.

2. **No compartir información sensible**: Asegúrate de no incluir datos sensibles como contraseñas o información privada en los commits. En caso de que accidentalmente subas información sensible a GitHub, elimina rápidamente el commit y actualiza el token de acceso.

3. **Validación de entrada de usuario**: Asegúrate de que los datos proporcionados por el usuario (como el número de commits o las fechas) sean válidos antes de procesarlos. Esto ayudará a evitar entradas maliciosas y errores que puedan comprometer la seguridad de los repositorios.

4. **Seguridad en Pull Requests y Issues**: Aunque este proyecto está enfocado en generar commits automatizados, los Pull Requests y Issues deben ser manejados cuidadosamente. Asegúrate de revisar y aprobar cualquier cambio antes de integrarlo al repositorio principal para evitar código malicioso o cambios no deseados.

5. **Revisión de seguridad periódica**: Realiza revisiones de seguridad periódicas para identificar posibles vulnerabilidades en el código y las dependencias. Mantén las bibliotecas actualizadas y sigue las mejores prácticas de seguridad en el desarrollo de software.

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
