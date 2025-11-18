from fastapi import FastAPI
from dotenv import load_dotenv
from routes.auth_routes import router as auth_router
from routes.predict_routes import router as predict_router

load_dotenv()

app = FastAPI(title="Emotion Detection API")


@app.get("/")
def home():
    return {"message": "Welcome to Emotion Detection API 👋"}


# Include routers
app.include_router(auth_router)
app.include_router(predict_router)
