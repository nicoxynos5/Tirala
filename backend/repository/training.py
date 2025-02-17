from database import execute_insert_not_injection, execute_query
from queries.training import query_create_training_25_shots, query_get_sessions_25_shots, query_get_percentages_25_shots, query_all_trainings
from utils.training import percentages_25_shots_processing


class TrainingRepository:

    def get_all_training(self):
        query = query_all_trainings()
        res = execute_query(query)
        plans = [dict(row) for row in res]
        return plans
    
    def create_training_25_shots(self, data):
        query, params = query_create_training_25_shots(data)
        execute_insert_not_injection(query, params)
    
    def get_sessions_25_shots(self, user_id):
        query = query_get_sessions_25_shots(user_id)
        res = execute_query(query)
        res = [dict(row) for row in res ]
        return res
    
    def get_percentages_25_shots(self, user_id):
        query = query_get_percentages_25_shots(user_id)
        res = execute_query(query)
        res = [dict(row) for row in res ]
        res_processed = percentages_25_shots_processing(res[0])
        return res_processed