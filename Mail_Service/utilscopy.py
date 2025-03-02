# from fastapi import FastAPI, Query
# from pydantic import BaseModel
# from email_service import send_verification_email
# from token_service import create_verification_token, verify_token

# app = FastAPI()

# class EmailRequest(BaseModel):
#     email: str

# @app.post("/send-email/")
# def send_email(request: EmailRequest):
#     token = create_verification_token(request.email)
#     return send_verification_email(request.email, token)

# @app.get("/verify/")
# def verify_email(token: str = Query(...)):
#     email = verify_token(token)
#     if email:
#         return {"message": f"{email} 이메일 인증 완료!"}
#     return {"error": "유효하지 않거나 만료된 토큰입니다."}
