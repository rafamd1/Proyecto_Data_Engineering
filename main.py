from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import openai
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.database import create_and_connect_database  # Asegúrate de que esta importación es correcta

# Inicialización de la aplicación FastAPI
app = FastAPI()

# Configuración de Jinja2 Templates
templates = Jinja2Templates(directory="app/templates")

# Montar los archivos estáticos (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configurar la clave de API de OpenAI
openai.api_key = ""

# Modelo de datos para la consulta
class Query(BaseModel):
    text: str

# Función para enviar la consulta al modelo de OpenAI (GPT-3.5-turbo)
def get_response(query: str) -> str:
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are the best poetic assistant, skilled in explaining complex programming concepts with creative flair. Write it in Spanish."},
                {"role": "user", "content": query}
            ]
        )
        # Ajuste para la estructura del objeto de respuesta
        if completion.choices and len(completion.choices) > 0:
            # Acceso correcto a la respuesta
            return completion.choices[0].message['content'].strip()
        return "No content found in response"
    except Exception as e:
        return f"Error: {e}"

@app.post("/query/")
async def query_endpoint(query: Query):
    try:
        response = get_response(query.text)
        
        # Guardar en MySQL
        connection = create_and_connect_database()
        if connection is not None:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO queries (query_text, response_text, timestamp)
                VALUES (%s, %s, NOW())
                """,
                (query.text, response)
            )
            connection.commit()
            cursor.close()
            connection.close()
        
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
