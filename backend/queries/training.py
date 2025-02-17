def query_all_trainings():
    return """
        SELECT name, duration
        FROM training_plans
        ORDER BY name DESC
    """

def query_create_training_25_shots(data):
    return """
        INSERT INTO training_25_shots (user_id, successful_shots, corner_left, corner_right, wing_left, wing_right, top_key, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """ ,(data.user_id, data.successful_shots, data.corner_left, data.corner_right, data.wing_left, data.wing_right, data.top_key, data.notes)

def query_get_sessions_25_shots(user_id):
    return f"""
        SELECT id, user_id, successful_shots, corner_left, corner_right, wing_left, wing_right, top_key, notes, TO_CHAR(created_at, 'DD/MM') as date
        FROM training_25_shots
        WHERE user_id = {user_id}
        ORDER BY date
    """

def query_get_percentages_25_shots(user_id):
    #con group by y avg
    return f"""
        SELECT 
            SUM(successful_shots) as successful_shots,
            count(*)*25 as total_shots,
            SUM(corner_left) as corner_left, 
            SUM(corner_right) as corner_right, 
            SUM(wing_left) as wing_left, 
            SUM(wing_right) as wing_right, 
            SUM(top_key) as top_key,
            count(*)*5 as shot_per_position
        FROM training_25_shots
        WHERE user_id = {user_id}
    """