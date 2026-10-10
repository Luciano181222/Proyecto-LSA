# Señas — Landing page funcional

Proyecto educativo construido con Python + Flask, HTML, CSS, JavaScript y SQLite.

## Incluye
- Landing page responsive con navegación por secciones: Inicio, Cómo funciona, Nosotros y Preguntas frecuentes.
- Modo claro/oscuro con preferencia guardada en el navegador.
- Registro e inicio de sesión reales con SQLite.
- Contraseñas guardadas con hash seguro (Werkzeug), no en texto plano.
- Sesión de usuario, cierre de sesión y ruta protegida `/traductor`.
- Vista de cámara funcional con permiso del navegador.
- Validación básica de datos y mensajes de estado.

## Requisitos
- Python 3.10 o superior.
- Navegador moderno.

## Instalación en Windows
1. Descomprimí el proyecto.
2. Abrí una terminal en la carpeta `senas_landing`.
3. Creá un entorno virtual (recomendado):
   ```powershell
   py -m venv .venv
   .venv\Scripts\activate
   ```
4. Instalá las dependencias:
   ```powershell
   pip install -r requirements.txt
   ```
5. Ejecutá:
   ```powershell
   python app.py
   ```
6. Abrí `http://127.0.0.1:5000`.

La base de datos `usuarios.db` se crea automáticamente al iniciar el servidor.

## Importante sobre el traductor
El inicio de sesión y el acceso a la cámara funcionan. La cámara es una vista previa: esta versión no afirma traducir señas automáticamente. Para lograrlo, conectá MediaPipe para extraer puntos de manos/cara y un modelo entrenado con datos de la lengua de señas que quieras reconocer. No existe un traductor fiable de todas las lenguas de señas sin entrenar y validar el modelo correspondiente.

## Para publicar
- Definí una variable de entorno `SECRET_KEY` con un valor aleatorio largo.
- Desactivá `debug=True` y usá un servidor WSGI adecuado.
- Serví el sitio mediante HTTPS para permitir acceso a la cámara.
- Para producción, agregá recuperación de contraseña, verificación de correo, límites de intentos y política de privacidad.
