def percentages_25_shots_processing(data):
    """
    Procesa los datos directos de la base de datos para obtener porcentajes y tiros totales
    """
    
    percentages = {}

    successful_shots = data.get("successful_shots", 0)
    total_shots = data.get("total_shots", 1)
    shot_per_position = data.get("shot_per_position", 1)

    positions = ["corner_left", "corner_right", "wing_left", "wing_right", "top_key"]

    for position in positions:
        tc_per_position = data.get(position, 0) # tiros convertidos por posición
        percentages[position] = {
            "avg_position" : round((tc_per_position / shot_per_position) * 100, 2), # porcentaje con 2 dec
            "total_shots" : shot_per_position
            }
    
    # Porcentaje de tiros totales (suma de todas las posiciones)
    percentages["total"] = {
        "avg_shots" : round((successful_shots / total_shots) * 100, 2),
        "total_shots" : total_shots
    }
    
    return percentages