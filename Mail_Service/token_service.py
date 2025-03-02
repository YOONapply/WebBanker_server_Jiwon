from datetime import datetime, timedelta
from jose import jwt, JWTError
from backend.Mail_Service.config import SECRET_KEY, ALGORITHM, TOKEN_EXPIRE_MINUTES

def create_verification_token(email: str):
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": email, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
