# Organiza2 - Gestor de Tareas y Productividad ✨

Organiza2 es una aplicación web desarrollada con Django diseñada para ayudarte a gestionar tus tareas, proyectos y mejorar tu productividad personal. Permite a los usuarios organizar sus actividades, establecer prioridades, etiquetar tareas y, potencialmente, colaborar con otros.

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.x-green.svg)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue.svg)](https://www.postgresql.org/)
[![Render](https://img.shields.io/badge/Deployed%20on-Render-orange)](https://render.com/)
<!-- Descomenta y actualiza estos cuando tengas el repo público y quieras usarlos:
[![GitHub issues](https://img.shields.io/github/issues/tu-usuario/Organiza2)](https://github.com/tu-usuario/Organiza2/issues)
[![GitHub forks](https://img.shields.io/github/forks/tu-usuario/Organiza2)](https://github.com/tu-usuario/Organiza2/network)
[![GitHub stars](https://img.shields.io/github/stars/tu-usuario/Organiza2)](https://github.com/tu-usuario/Organiza2/stargazers)
-->

## Tabla de Contenidos

1.  [Acerca del Proyecto](#acerca-del-proyecto)
    *   [Motivación](#motivación)
2.  [Características Principales](#características-principales)
3.  [Tecnologías Utilizadas](#tecnologías-utilizadas)
4.  [Estructura del Proyecto](#estructura-del-proyecto)
5.  [Puesta en Marcha](#puesta-en-marcha)
    *   [Prerrequisitos](#prerrequisitos)
    *   [Instalación Local](#instalación-local)
6.  [Despliegue](#despliegue)
7.  [Uso](#uso)
8.  [Contribuciones](#contribuciones)
9.  [Licencia](#licencia)
10. [Contacto](#contacto)

## Acerca del Proyecto

Organiza2 busca ofrecer una herramienta intuitiva y eficiente para la gestión de tareas diarias y proyectos. La plataforma permite a los usuarios crear, organizar y seguir el progreso de sus actividades, con funcionalidades pensadas para mejorar la productividad individual.

### Motivación

Este proyecto fue desarrollado con varios propósitos en mente:
*   Como **Trabajo Final de Grado (TFG)**.
*   Para crear una **aplicación útil y personalizable** para la gestión personal.
*   Para **desarrollar habilidades** en tecnologías web modernas como Django, PostgreSQL, y plataformas de despliegue como Render.

## Características Principales 🚀

*   **Autenticación de Usuarios:** Registro, inicio de sesión y cierre de sesión seguros.
*   **Gestión Completa de Tareas (CRUD):**
    *   Creación de nuevas tareas con título, descripción, fecha de vencimiento, estado, visibilidad y prioridad.
    *   Listado de tareas personales.
    *   Edición de tareas existentes.
    *   Eliminación de tareas.
    *   Visualización detallada de cada tarea.
*   **Perfiles de Usuario:** Espacio personal para cada usuario donde se podrá hace el CRUD de las tareas.
*   **Etiquetas Dinámicas para Tareas:** Los usuarios pueden asignar etiquetas existentes o crear nuevas sobre la marcha para categorizar sus tareas.
*   **Foro:** Una sección básica de foro para la interacción entre usuarios (funcionalidad inicial).
*   **Interfaz Amigable:** Diseño limpio y funcional con CSS personalizado.
*   **Despliegue en la Nube:** Listo para ser desplegado en plataformas como Render.

## Tecnologías Utilizadas 🛠️

*   **Backend:**
    *   Python 3.13.2
    *   Django 5.2.1
*   **Frontend:**
    *   HTML5
    *   CSS3
    *   JavaScript (para funcionalidades como el selector de etiquetas TomSelect)
*   **Base de Datos:**
    *   PostgreSQL (para producción)
    *   SQLite3 (para desarrollo local)
*   **Despliegue:**
    *   Render (para la aplicación principal Django)
    *   GitHub Pages (para el despliegue de contenido estático a través de GitHub Actions)
*   **Control de Versiones:**
    *   Git
    *   GitHub
*   **Herramientas Adicionales:**
    *   TomSelect.js: Para la selección y creación de etiquetas de forma dinámica.
    *   Gunicorn: Servidor WSGI para producción.

## Estructura del Proyecto

La estructura del proyecto sigue las formas de Django:

*   `proyectoTFG/`: Contiene la configuración principal del proyecto Django (`settings.py`, `urls.py`, `wsgi.py`, `asgi.py`).
*   `Organiza2/`: Es la aplicación Django principal que contiene:
    *   `models.py`: Definición de los modelos de la base de datos (Tarea, PerfilUsuario, Etiqueta, ComentarioTarea).
    *   `views.py`: Lógica de las vistas (funciones y clases que manejan las peticiones HTTP).
    *   `forms.py`: Formularios de Django para la entrada de datos (TareaForm).
    *   `urls.py`: Rutas URL específicas de la aplicación Organiza2.
    *   `templates/`: Plantillas HTML para la interfaz de usuario.
    *   `static/`: Archivos estáticos (CSS, JavaScript, imágenes).
    *   `migrations/`: Migraciones de la base de datos generadas por Django.
    *   `admin.py`: Configuración para el panel de administración de Django.
*   `.github/workflows/static.yml`: Workflow de GitHub Actions para desplegar contenido estático.
*   `manage.py`: Utilidad de línea de comandos de Django.
*   `Procfile`: Para la configuración de despliegue Render (especifica el comando web con Gunicorn).
*   `render.yaml`: Archivo de configuración "Infrastructure as Code" para desplegar en Render.
*   `.gitignore`: Especifica los archivos y directorios que Git debe ignorar.
*   `requirements.txt` (No provisto en el Markdown, pero esencial): Debería listar todas las dependencias de Python.


## Puesta en Marcha

Para ejecutar este proyecto localmente, sigue estos pasos:

### Prerrequisitos

*   Python 3.8 o superior
*   pip (gestor de paquetes de Python)
*   Git
*   (Opcional) PostgreSQL instalado y configurado si deseas usarlo localmente en lugar de SQLite.

### Instalación Local

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/SamuelRomeroUber/Organiza2.git
    cd Organiza2
    ```

2.  **Crea y activa un entorno virtual:**
    ```bash
    python -m venv venv
    # En Windows
    venv\Scripts\activate
    # En macOS/Linux
    source venv/bin/activate
    ```

3.  **Instala las dependencias:**
    (Asegúrate de tener un archivo `requirements.txt` con todas las dependencias como Django, dj-database-url, gunicorn, psycopg2-binary, etc.)
    ```bash
    pip install -r requirements.txt
    ```
    *Si no tienes `requirements.txt`, necesitarás instalar las dependencias manualmente:*
    ```bash
    pip install Django dj_database_url gunicorn psycopg2-binary Pillow # Pillow para ImageField
    ```

4.  **Configura la base de datos:**
    Por defecto, usará SQLite. Si quieres usar PostgreSQL localmente, necesitarás:
    *   Crear una base de datos PostgreSQL.
    *   Configurar las variables de entorno `DATABASE_URL` o modificar `proyectoTFG/settings.py`.

5.  **Aplica las migraciones:**
    ```bash
    python manage.py migrate
    ```

6.  **Crea un superusuario (opcional, para acceder al admin):**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Ejecuta el servidor de desarrollo:**
    ```bash
    python manage.py runserver
    ```
    La aplicación estará disponible en `http://127.0.0.1:8000/`.

## Despliegue ☁️

La aplicación está configurada para un despliegue sencillo en **Render** utilizando el archivo `render.yaml`. Render leerá este archivo para configurar el entorno, construir el proyecto e iniciar la aplicación.

También se incluye un archivo `.github/workflows/static.yml` que muestra un ejemplo de cómo desplegar contenido estático a GitHub Pages, aunque la aplicación Django principal está diseñada para ser servida desde una plataforma como Render.

## Uso

Una vez que la aplicación esté en funcionamiento (localmente o desplegada):

1.  **Regístrate:** Crea una nueva cuenta de usuario.
2.  **Inicia Sesión:** Accede con tus credenciales.
3.  **Perfil de Usuario:** Desde tu perfil, podrás:
    *   Crear nuevas tareas.
    *   Ver la lista de tus tareas.
    *   Editar o eliminar tareas existentes.
4.  **Foro:** Explora la sección del foro para interactuar.
<!--
## Contribuciones 🤝

Las contribuciones son bienvenidas. Si deseas mejorar Organiza2:

1.  Haz un Fork del proyecto.
2.  Crea tu Feature Branch (`git checkout -b feature/AmazingFeature`).
3.  Haz Commit de tus cambios (`git commit -m 'Add some AmazingFeature'`).
4.  Haz Push a la Branch (`git push origin feature/AmazingFeature`).
5.  Abre un Pull Request.

Para cambios mayores, por favor abre un issue primero para discutir lo que te gustaría cambiar.
 -->
## Contacto 📧

Samuel Romero Uber - samueldelatorreuber2517@gmail.com

Enlace al Proyecto: [https://github.com/SamuelRomeroUber/ProyectoTFG.git](https://github.com/SamuelRomeroUber/ProyectoTFG.git)
