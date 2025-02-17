import matplotlib.pyplot as plt
import io
import base64


def generate_graphs_per_position(sessions):
    graphs = []
    corner_left, corner_right, wing_left, wing_right, top_key = [], [], [], [], []

    for session in sessions:
        corner_left.append(session['corner_left'])
        corner_right.append(session['corner_right'])
        wing_left.append(session['wing_left'])
        wing_right.append(session['wing_right'])
        top_key.append(session['top_key'])
    

    dates = [session['date'] for session in sessions]

    # Graficamos cada tipo de tiro en gráficos independientes
    for y_data, label in zip([corner_left, corner_right, wing_left, wing_right, top_key], 
                             ['Corner izquierdo', 'Corner derecho', '45° izquierdo', '45° derecho', 'Eje central']):
        plt.figure()
        plt.plot(dates, y_data, marker='o')
        plt.title(label)
        plt.xlabel('Fecha', labelpad=15)
        plt.ylabel('Conversiones', labelpad=15)
        plt.xticks(rotation=45)
        plt.grid()
        plt.tight_layout()

        # Guardar el gráfico en memoria
        img_stream = io.BytesIO()
        plt.savefig(img_stream, format='png')
        img_stream.seek(0)  # Mover el puntero al inicio del archivo en memoria
        plt.close()

        # Convertir la imagen a base64
        img_base64 = base64.b64encode(img_stream.getvalue()).decode('utf-8')
        graphs.append({'label': label, 'image': img_base64})  # Guardamos el label y la imagen en base64

    return graphs