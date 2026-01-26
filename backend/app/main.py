from fastapi import FastAPI
from app.router import evaluate
from app.router import featureflag

app = FastAPI()

app.include_router(evaluate.router)
app.include_router(featureflag.router)

