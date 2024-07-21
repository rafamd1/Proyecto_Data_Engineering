from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from langchain_core.prompts import PromptTemplate
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.database import create_and_connect_database  # Asegúrate de que esta importación es correcta

# Inicialización de la aplicación FastAPI
app = FastAPI()

# Configuración de Jinja2 Templates
templates = Jinja2Templates(directory="app/templates")

# Montar los archivos estáticos (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Cargar el tokenizador y el modelo de HuggingFace
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")

# Modelo de datos para la consulta
class Query(BaseModel):
    text: str

# Función para enviar la consulta al modelo de lenguaje
def get_response(query: str) -> str:
    prompt = PromptTemplate(template="User: {query}\nAssistant:", input_variables=["query"])
    formatted_prompt = prompt.format(query=query)
    inputs = tokenizer.encode(formatted_prompt, return_tensors="pt")
    outputs = model.generate(inputs, max_length=150, num_beams=5, early_stopping=True)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

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
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)