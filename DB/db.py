import mysql.connector



# MariaDB 연결 정보 설정
config = {
    "host": "svc.sel4.cloudtype.app",
    "user": "root",         
    "password": "Awdzsc010!@dbr",     
    "database": "wbDB",
    "port": 30468 
}

try:
    # 데이터베이스 연결
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # 테이블 생성 예제
    cursor.execute("""
        CREATE DATABASE test2
    """)
    conn.commit() # 적용하기

    # # 데이터 삽입
    # query = "INSERT INTO Users (username, email) VALUES (%s, %s)"
    # values = ("test_user", "test@example.com")
    # cursor.execute(query, values)
    # conn.commit()

    # # 데이터 조회 예제
    # cursor.execute("SELECT * FROM Users")
    # results = cursor.fetchall()
    # for row in results:
    #     print(row)

    # 연결 종료
    cursor.close()
    conn.close()

except mysql.connector.Error as e:
    print(f"❌ MySQL 연결 실패: {e}")