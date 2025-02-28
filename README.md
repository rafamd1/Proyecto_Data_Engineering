# Proyecto Data Engineering: Desarrollo de una Aplicación de IA Generativa

## Descripción del Proyecto
El objetivo es desarrollar una aplicación web que integre un modelo de lenguaje generativo para ofrecer una experiencia interactiva con los usuarios. La aplicación utiliza Python y FastAPI para interactuar con el modelo **3.5 turbo de ChatGPT**, dándole un prompt inicial para que genere respuestas a problemas de programación en el formato de un poema en español. Los usuarios podrán enviar consultas a través de la API y recibir respuestas generadas por el modelo. Las interacciones serán registradas en una base de datos desplegada en AWS para mantener un historial completo de consultas y respuestas.

## Objetivos
- Desarrollo de Aplicación Web: Construir una aplicación web con Python y FastAPI que permita la interacción con modelos de lenguaje.
- Integración con Modelos de Lenguaje: Utilizar el modelo 3.5 turbo de ChatGPT para generar respuestas a partir de consultas.
- Registro en Base de Datos: Configurar una base de datos en AWS para almacenar un histórico de las interacciones.
- Dockerización: Empaquetar la aplicación en un contenedor Docker para facilitar su despliegue y escalabilidad.

## Temática y Caso de Uso
El proyecto permite adaptar el modelo a cualquier caso de uso relevante. Algunas posibles ideas incluyen:

- Asistente Virtual: Un asistente que responda consultas comunes sobre productos o servicios.
- Generación de Texto: Una herramienta para redactar artículos o informes según necesidades específicas.
- Sistema de Recomendación: Recomendaciones de películas, libros o música basadas en preferencias del usuario.
- Chatbot Educativo: Un chatbot que responda a preguntas sobre temas académicos o de aprendizaje.
