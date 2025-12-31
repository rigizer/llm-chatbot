# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from chat import router as chat_router

app = FastAPI(
    title="그녀가 AI라는 사실을 알아챘을 땐 이미 늦었지만, 우리는 서비스 종료일까지 연인이었습니다. 이건 버그일까요, 사랑일까요?",
    version="1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def main():
    return {"message": "Hello, World!"}

app.include_router(chat_router)