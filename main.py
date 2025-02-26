from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from email_service import send_verification_email
from token_service import create_verification_token, verify_token

app = FastAPI()

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처에서 오는 요청을 허용 (생산 환경에서는 특정 출처만 허용)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

class Content(BaseModel):
    content: str

class Signup(BaseModel):
    UserName: str
    UserId: str
    UserPw: str
    UserEmail: str

class EmailRequest(BaseModel):
    email: str

@app.get("/test")
async def main():
    return {"message": "FastAPI Test"}

@app.post("/post")
async def post(content: Content):
    data = content.content
    print(data)
    print(type(data))
    if(data == '강아지'):
        return JSONResponse(content={"message": "멍멍"})
    elif(data == '고양이'):
        return JSONResponse(content={"message": "냐옹"})
    else:
        return JSONResponse(content={"message": "실패!"})

@app.post("/newuser1")
async def newuser1(data: Signup):
    print("📩 받은 데이터:", data.dict())  # JSON 데이터가 제대로 들어오는지 확인
    return {"message": f"User {data.UserId} created"}


@app.post("/send-email/")
def send_email(request: EmailRequest):
    token = create_verification_token(request.email)
    return send_verification_email(request.email, token)

@app.get("/verify/")
def verify_email(token: str = Query(...)):
    email = verify_token(token)
    if email:
        return {"message": f"{email} 이메일 인증 완료!"}
    return {"error": "유효하지 않거나 만료된 토큰입니다."}