from database import execute_query, execute_not_injection, execute_insert_not_injection, execute_query_not_injection
from queries.user import query_user_exists, query_create_user, query_get_user_by_email, query_get_user_password_by_email

class UserRepository:
    def user_exists(self, user_email):
        query = query_user_exists()
        result = execute_query_not_injection(query, (user_email, ))
        return result[0]['exists'] #True or False

    def create_user(self, data):
        query, params = query_create_user(data)
        execute_insert_not_injection(query, params)

    def get_user_by_email(self, email):
        query, params = query_get_user_by_email(email)
        result = execute_query_not_injection(query, params)
        return result[0] if result else None
    
    def get_user_password_by_email(self, email):
        query, params = query_get_user_password_by_email(email)
        result = execute_query_not_injection(query, params)
        return result[0]['password'] if result else None
