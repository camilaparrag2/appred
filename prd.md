Markdown
# Product Requirement Document (PRD) - FeedPlan

## 1. Información del Documento
* **Autor:** Emprendedor / Desarrollador
* **Estado:** Borrador Inicial
* **Tecnologías:** Django 6.0, SQLite, Tailwind CSS (CDN), Render

---

## 2. Objetivos del Producto
El objetivo es construir una aplicación web ligera y enfocada en la UX que permita a los emprendedores visualizar estéticamente sus publicaciones de redes sociales y agendar su contenido semanal sin la fricción de herramientas de diseño complejas.

### Objetivos Específicos:
1. Proporcionar un espejo visual (mockup) fidedigno de los feeds de Instagram, Facebook y TikTok.
2. Permitir el ordenamiento visual de las imágenes subidas.
3. Ofrecer una agenda semanal interactiva para organizar los formatos (Imagen, Carrusel, Reel).

---

## 3. Requisitos Funcionales

### RF-01: Autenticación de Usuarios
* El sistema debe permitir el registro con nombre de usuario, email y contraseña.
* El sistema debe validar las credenciales en el inicio de sesión.
* Cada usuario solo puede ver y editar sus propias imágenes y agenda.

### RF-02: Simulador Visual de Feeds
* El usuario podrá subir imágenes en formato JPG/PNG.
* El usuario podrá alternar entre tres vistas mediante pestañas:
  * **Instagram:** Vista de cuadrícula clásica.
  * **Facebook:** Línea de tiempo vertical.
  * **TikTok:** Cuadrícula vertical de 3 columnas optimizada para formato largo.

### RF-03: Agenda Semanal
* Vista de cuadrícula de 7 días (Lunes a Domingo).
* Botón para agregar un "Post Borrador".
* Formulario para seleccionar el tipo de post: Imagen, Carrusel, Reel.
* Opción de modificar o mover el día del post planificado.

---

## 4. Requisitos No Funcionales y Técnicos

* **Backend:** Django 6.0 utilizando estrictamente **Vistas Basadas en Funciones (FBVs)**.
* **Base de Datos:** SQLite local. En Render se implementará un volumen persistente para no perder los datos.
* **Estilos:** Tailwind CSS integrado por CDN para mantener el proyecto rápido y limpio de compiladores pesados.
* **Documentación:** Todo archivo crítico de Python (`models.py`, `views.py`, `urls.py`) debe llevar docstrings detallando su propósito.
* **Control de Cambios:** Se mantendrá una carpeta `/docs` con archivos Markdown para registrar el progreso y la hoja de ruta.

---

## 5. Diseño de Modelos de Datos

### Modelo: MediaPost
```python
# planner/models.py
from django.db import models
from django.contrib.auth.models import User

class MediaPost(models.Model):
    """
    Almacena las imágenes que el usuario sube para previsualizar en sus feeds.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='feeds/')
    order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-uploaded_at']