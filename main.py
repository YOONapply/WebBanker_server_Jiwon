# Import #########################################################################################
from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
# from Mail_Service.email_service import send_verification_email
# from Mail_Service.token_service import create_verification_token, verify_token
import mysql.connector
from contextlib import contextmanager
##################################################################################################



# . ##############################################################################################
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처에서 오는 요청을 허용 (생산 환경에서는 특정 출처만 허용)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)
##################################################################################################



# DB #############################################################################################
# fetchall()	모든 결과를 리스트로 반환 (List[Tuple])
# fetchone()	결과 중 첫 번째 행만 반환 (Tuple)
# fetchmany(n)	최대 n개의 행을 리스트로 반환 (List[Tuple])

config = {
    "host": "svc.sel4.cloudtype.app",
    "user": "root",         
    "password": "Awdzsc010!@dbr",     
    "database": "wbDB",
    "port": 30468 
}

# 전역 변수 (연결 유지)
conn = None  

def DBconn(): # DB 연결 함수
    global conn
    if conn is None or not conn.is_connected():
        conn = mysql.connector.connect(**config)
    return conn

@contextmanager
def DBcursor(): # DB 커서 함수 / 종료 -> 자동으로 커서 반환 
    cursor = DBconn().cursor()
    try:
        yield cursor  
    finally:
        cursor.close() 
##################################################################################################



# Login & Signup #################################################################################
# Login
@app.post("/userlogin")
async def userlogin(request: Request):
    try:
        data = await request.json()
        UserId = data["UserId"]
        UserPw = data["UserPw"]
    except:
        return{"Success" : False, "ErrorCode" : "dataerr"}
    
        
    with DBcursor() as cursor:
        try:
            ########## 유저 아이디 검사 ##########
            cursor.execute("SELECT EXISTS(SELECT 1 FROM Users WHERE UserId = %s)", (UserId,))
            result = cursor.fetchone()
            
            # 유저 아이디 존재
            if result[0]:

                ########## 비번 일치 검사 ##########
                cursor.execute("SELECT UserPw FROM Users WHERE UserId = %s ", (UserId,))
                result = cursor.fetchone()
        
                # 비번 일치
                if result[0] == UserPw:
                    cursor.execute("SELECT UserName FROM Users WHERE UserId = %s", (UserId,))
                    result = cursor.fetchone()
                    UserName = result[0]
                    return {"Success": True, "UserName": UserName}    
                # 비번 불일치
                else:
                    return {"Success": False, "ErrorCode": "pwerror"}
            
                
            # 유저 아이디 존재 X
            else:
                return {"Success": False, "ErrorCode": "pwerror"}
            
        except:
            return {"Success": False, "ErrorCode": "NONE"}



    # try:
    #     if data["UserId"] != TempData["UserId"]:
    #         return {"Success" : False, "ErrorCode" : "iderror"}
    #     if data["UserPw"] != TempData["UserPw"]:
    #         return {"Success" : False,"ErrorCode" : "pwerror"}
    #     return {"Success" : True}
    # except:
    #     return {"Success" : False}

# Signup
@app.post("/newuser1") 
async def newuser1(request: Request):
    try:  
        data = await request.json()     
        UserId = data["UserId"]
        UserAccount = "-1"
        UserPw = data["UserPw"]
        UserPwRe = data["UserPwRe"]
        UserName = data["UserName"]       
        UserEmail = data["UserEmail"]

    except:
        return {"Success" : False, "ErrorCode" : "dataerr"}
    
    try:
        with DBcursor() as cursor:
            try:    
                # User 존재 여부 조회
                cursor.execute("SELECT EXISTS(SELECT 1 FROM Users WHERE UserId = %s)", (UserId,))

                # 결과 받아오기
                result = cursor.fetchone()

                ########## 아이디 중복 X ####################
                if not result[0]: 
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print("존재하지 않는 ID입니다. 회원가입을 진행합니다.")
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

                    try:
                        ########## 비밀번호 일치 ##########
                        if UserPw == UserPwRe:
                            query = "INSERT INTO Users (UserId, UserAccount, UserPw, UserEmail, UserName) VALUES (%s, %s, %s, %s, %s);"
                            values = (UserId, UserAccount, UserPw, UserEmail, UserName)

                            cursor.execute(query, values)
                            conn.commit() 

                            return {"Success": True, "UserName": UserName}
                    
                        ################################



                        ########## 비밀번호 불일치 ##########
                        else:
                            return {"Success": False, "ErrorCode": "n-samepw"}
                        #################################
                        
                    except:
                        return {"Success": False, "ErrorCode": "NONE"}                    
                ##########################################



                ########## 아이디 중복 O ####################
                else:
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print("존재하는 ID")
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    return {"Success" : False, "ErrorCode" : "sameid"}    
                ##############################################

            except: 
                return {"Success": False, "ErrorCode": "NONE"}
            



            

            # if data["UserPw"] != data["UserPwRe"]:
                
            
    except:
        return{"Success" : False, "ErrorCode": "NONE"}
##################################################################################################



# # Mail Service ###################################################################################
# @app.post("/send-email/")
# def send_email(request: Request):
#     token = create_verification_token(request.email)
#     return send_verification_email(request.email, token)

# @app.get("/verify/")
# def verify_email(token: str = Query(...)):
#     email = verify_token(token)
#     if email:
#         return {"message": f"{email} 이메일 인증 완료!"}
#     return {"error": "유효하지 않거나 만료된 토큰입니다."}
# ##################################################################################################