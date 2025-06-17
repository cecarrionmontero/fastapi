from conn.mysql_conn import get_connection

def call_stored_procedure(sp_name, payload, param_names):
    conn = get_connection()
    with conn.cursor() as cursor:
        args = [payload.get(name) for name in param_names]
        cursor.callproc(sp_name, args)
        result = cursor.fetchall()
    conn.close()
    return result

def get_all_procedures_and_params():
    conn = get_connection()
    sp_dict = {}

    with conn.cursor() as cursor:
        # Obtener todos los SPs (aunque no tengan parámetros)
        cursor.execute("""
            SELECT ROUTINE_NAME
            FROM information_schema.ROUTINES
            WHERE ROUTINE_SCHEMA = DATABASE() AND ROUTINE_TYPE = 'PROCEDURE'
        """)
        sps = [row["ROUTINE_NAME"] for row in cursor.fetchall()]

        # Obtener los parámetros
        cursor.execute("""
            SELECT SPECIFIC_NAME, PARAMETER_NAME
            FROM information_schema.PARAMETERS
            WHERE SPECIFIC_SCHEMA = DATABASE()
            ORDER BY SPECIFIC_NAME, ORDINAL_POSITION
        """)
        param_rows = cursor.fetchall()

    conn.close()

    for sp in sps:
        sp_dict[sp] = []

    for row in param_rows:
        sp_name = row["SPECIFIC_NAME"]
        param = row["PARAMETER_NAME"]
        if param:
            sp_dict[sp_name].append(param)

    return sp_dict

