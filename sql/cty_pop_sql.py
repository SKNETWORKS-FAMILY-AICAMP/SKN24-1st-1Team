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

def insert_cty_pop(value_list) :
    connection, cursor = connect_db()
    success = 0
    if connection.is_connected():
        sql = "DELETE FROM tbl_cty_pop"
        cursor.execute(sql)
        
        sql = """
                INSERT INTO tbl_cty_pop
                (CTY_CODE, CTY_POP_YR, CTY_POP)
                VALUES((SELECT CTY_CODE FROM tbl_cty WHERE CTY_NM = %s), %s, %s)
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

def select_cty_pop(where_dict=None):
    connection, cursor = connect_db()
    rows = []
    if connection.is_connected():
        sql = """
                SELECT
                    (SELECT CTY_NM FROM tbl_cty WHERE CTY_CODE = a.CTY_CODE)
                    , CTY_POP_YR 
                    , CTY_POP
                FROM tbl_cty_pop a
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