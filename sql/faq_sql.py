import mysql.connector

def connect_db() :
    connection = mysql.connector.connect(
        host = 'localhost'          # MySQL 서버 주소 (ip)
        , user = 'ohgiraffers'      # 사용자 이름
        , password = 'ohgiraffers'  # 비밀번호
        , database = 'roadkeeperdb' # 사용할 DB 스키마
    )
    cursor = connection.cursor()
    return connection, cursor

def insert_faq(value_list, inst_nm) :
    connection, cursor = connect_db()
    success = 0
    if connection.is_connected():
        sql = "DELETE FROM tbl_faq WHERE INST_NM = '" + inst_nm + "'"
        cursor.execute(sql)
        
        sql = """
                INSERT INTO tbl_faq
                (QUESTION, ANSWER, INST_NM)
                VALUES(%s, %s, %s)
                """
        for values in value_list :
            try :
                cursor.execute(sql, values)
                success += cursor.rowcount
            except :
                print('pass된 data : ', values)
    connection.commit()
    cursor.close()
    connection.close()
    return success

def select_faq(where_dict=None):
    connection, cursor = connect_db()
    rows = []
    if connection.is_connected():
        sql = """
                SELECT
                    QUESTION, ANSWER, INST_NM
                FROM tbl_faq
            """
        params = []

        if where_dict:
            conditions = []
            for k, v in where_dict.items():
                conditions.append(f"{k} = %s")
                params.append(v)
            sql += " WHERE " + " AND ".join(conditions)

        cursor.execute(sql, params)
        rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows