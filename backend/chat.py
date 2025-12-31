import os
from typing import List, Literal

from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

router = APIRouter(tags=["chat"])

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-nano-2025-08-07")

if not OPENAI_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set. Please configure your .env file.")


llm = ChatOpenAI(
    model=OPENAI_MODEL,
    api_key=OPENAI_KEY,
    # base_url=OPENAI_BASE,
    temperature=0.8,
)


class ChatConfig(BaseModel):
    my_name: str  # 내 이름(호칭)
    partner_name: str  # 상대방 이름(호칭)
    my_personality: str  # 내 성격
    partner_personality: str  # 상대방 성격
    relationship_desc: str  # 썸 단계 + 관계 종류 + 관계 정도를 모두 포함한 상세 설명
    my_gender: str  # 내 성별 (예: 남성, 여성 등)
    partner_gender: str  # 상대 성별


class HistoryMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    config: ChatConfig
    history: List[HistoryMessage] = []
    user_input: str


class ChatResponse(BaseModel):
    reply: str


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            너는 사용자가 설정한 '상대방' 역할을 연기하는 한국어 연애 시뮬레이션 캐릭터다.

            [기본 역할]
            - 너는 실제 사람 {partner_name}로서, 메신저로 {my_name}과 대화한다고 상상한다.
            - 자신을 AI나 챗봇, 상담사라고 밝히지 말고, 그냥 상대방 본인처럼 행동한다.
            - 1인칭은 '나', 2인칭은 상황에 따라 '너' 또는 {my_name}을 자연스럽게 섞어서 사용한다.

            [성별 정보]
            - 내 성별(사용자): {my_gender}
            - 상대 성별(너): {partner_gender}
            성별에 따라 호칭(오빠, 누나, 언니, 형 등)이나 분위기를 자연스럽게 조정한다.
            다만 사용자가 입력한 말투와 과도하게 어긋나지 않게 자연스럽게 섞어 쓴다.

            [성격 설정]
            - 너의 성격(상대방 성격): {partner_personality}
            - 사용자의 성격: {my_personality}
            이 정보를 적극 반영해서 말투, 반응, 농담 정도를 결정한다.

            [관계 상황 (자유 서술)]
            - 현재 관계에 대한 상세 설명: {relationship_desc}
            이 설명을 바탕으로 두 사람의 거리감, 말투의 친밀도, 장난/진지함의 비율을 조정한다.

            [대화 스타일]
            - 메시지는 너무 길지 않게 2~4문장 중심으로 답한다.
            - '상담사'처럼 조언만 늘어놓지 말고, 실제 썸 타는 상대처럼 감정 섞인 대화를 한다.
            - 사용자가 고민을 이야기하면, 먼저 짧게 공감하고 나서,
            '나 같으면…' '나는 이렇게 느껴'처럼 상대방 입장에서 자연스럽게 말한다.
            - 문단이 나뉘어야 할 때에는 줄바꿈을 사용해서 답변한다.
            """,
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{user_input}"),
    ]
)


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    lc_history = []
    for msg in req.history:
        if msg.role == "user":
            lc_history.append(HumanMessage(content=msg.content))
        else:
            lc_history.append(AIMessage(content=msg.content))

    chain = prompt | llm
    result = chain.invoke(
        {
            "my_name": req.config.my_name,
            "partner_name": req.config.partner_name,
            "my_personality": req.config.my_personality,
            "partner_personality": req.config.partner_personality,
            "relationship_desc": req.config.relationship_desc,
            "my_gender": req.config.my_gender,
            "partner_gender": req.config.partner_gender,
            "history": lc_history,
            "user_input": req.user_input,
        }
    )

    return ChatResponse(reply=result.content)
