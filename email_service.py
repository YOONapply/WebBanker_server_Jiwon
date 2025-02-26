import smtplib # SMTP 서버와 연결하여 메일을 보낵 위한 모듈
from email.mime.text import MIMEText # 메일 본문을 작성하는 모듈
from email.mime.multipart import MIMEMultipart # 메일에 제목, 본문 등을 포함할 수 있게 지원
from config import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD # 환경변수 가져오기

def send_verification_email(receiver_email: str, token: str):
    """ 사용자의 이메일로 인증 링크를 전송하는 함수 """

    # 1. 이메일 제목과 인증 링크 생성
    subject = "이메일 인증 요청" # 이메일 제목
    verification_link = f"http://localhost:8000/verify?token={token}" # 인증 링크

    # 2. 이메일 메시지 구성
    message = MIMEMultipart() # 이메일 객체 생성
    message["From"] = SENDER_EMAIL # 보내는 사람 설정
    message["To"] = receiver_email # 받는 사람 설정
    message["Subject"] = subject # 제목 설정

    # 3. 이메일 본문 작성
    body = f"이메일 인증을 완료하려면 아래 링크를 클릭하세요:\n{verification_link}"
    message.attach(MIMEText(body, "plain")) # 본문 추가

    try:
        # 4. SMTP 서버에 연결
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls() # TLS 보안 연결 활성화
            server.login(SENDER_EMAIL, SENDER_PASSWORD) # 이메일 계정 로그인
            server.sendmail(SENDER_EMAIL, receiver_email, message.as_string()) # 이메일 전송
        return {"message": "인증 이메일이 발송되었습니다."}
    except Exception as e:
        return {"error": str(e)} # 오류 발생 시 메시지 반환
