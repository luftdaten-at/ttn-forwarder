from fastapi import FastAPI

# Create a FastAPI application instance
app = FastAPI()

# Define your endpoints and their handlers
@app.get("/")
def root():
    return {"message": "Hello, FastAPI!"}