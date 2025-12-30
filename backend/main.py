from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def main():
    return {"message": "Welcome"}

@app.get("/hello")
def hello():
    return {"message": "Hello World"}