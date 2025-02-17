def query_user_exists():
    return """
        SELECT EXISTS (
            SELECT 1
            FROM users
            WHERE email = %s
        )
    """


def query_create_user(data):
    return """
        INSERT INTO users (email, first_name, last_name, password, birth_date, role)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (data.email, data.first_name, data.last_name, data.password, data.birth_date, data.role)


def query_get_user_by_email(email):
    return """
        SELECT id, email, first_name, last_name, birth_date, role
        FROM users
        WHERE email = %s
    """, (email,)

def query_get_user_password_by_email(email):
    return """
        SELECT password
        FROM users
        WHERE email = %s
    """, (email,)
