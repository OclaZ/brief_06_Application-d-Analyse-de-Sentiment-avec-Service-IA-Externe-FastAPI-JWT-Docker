from fastapi import FastAPI
from dotenv import load_dotenv
from routes.auth_routes import router as auth_router
from routes.predict_routes import router as predict_router
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(title="Emotion Detection API")

origins = [
    "http://localhost:3000",  # Next.js dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # or ["*"] during development
    allow_credentials=True,
    allow_methods=["*"],            # VERY IMPORTANT (allows OPTIONS)
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Welcome to Emotion Detection API 👋"}


# Include routers
app.include_router(auth_router)
app.include_router(predict_router)
