# sql/cty_pop_sql.py
import mysql.connector

def connect_db():
    connection = mysql.connector.connect(
        host='localhost',
        user='ohgiraffers',
        password='ohgiraffers',
        database='roadkeeperdb',
        charset='utf8mb4',
        collation='utf8mb4_general_ci'
    )
    cursor = connection.cursor()
    return connection, cursor


def select_cty_pop(year=None, cty_codes=None):
    """
    year: int | None
    cty_codes: list[int] | None
    return: list[tuple] -> (CTY_NM, CTY_POP_YR, CTY_POP)
    """
    connection, cursor = connect_db()
    rows = []

    if connection.is_connected():
        sql = """
            SELECT
                c.CTY_NM,
                a.CTY_POP_YR,
                a.CTY_POP
            FROM tbl_cty_pop a
            JOIN tbl_cty c ON c.CTY_CODE = a.CTY_CODE
        """
        conditions = []
        params = []

        if year is not None:
            conditions.append("a.CTY_POP_YR = %s")
            params.append(year)

        if cty_codes:
            placeholders = ",".join(["%s"] * len(cty_codes))
            conditions.append(f"a.CTY_CODE IN ({placeholders})")
            params.extend(cty_codes)

        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        sql += " ORDER BY a.CTY_POP DESC"

        cursor.execute(sql, params)
        rows = cursor.fetchall()

    cursor.close()
    connection.close()
    return rows


def fetch_year_list():
    connection, cursor = connect_db()
    cursor.execute("""
        SELECT DISTINCT CTY_POP_YR
        FROM tbl_cty_pop
        ORDER BY CTY_POP_YR
    """)
    years = [row[0] for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return years


def fetch_city_list():
    connection, cursor = connect_db()
    cursor.execute("""
        SELECT CTY_CODE, CTY_NM
        FROM tbl_cty
        ORDER BY CTY_NM
    """)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows