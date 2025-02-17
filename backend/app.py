from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, trainings


app = FastAPI(title="Tirala",
              description="Aplicación de basquet para entrenar el tiro")

app.include_router(users.router)
app.include_router(trainings.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Todos los métodos
    allow_headers=["*"],  # " encabezados
)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a Tirala"}