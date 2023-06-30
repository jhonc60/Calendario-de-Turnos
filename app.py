from flask import Flask, render_template
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def index():
    hoy = datetime.now()
    año = hoy.year
    dias_restantes = (datetime(año + 1, 1, 1) - hoy).days

    turnos = generar_turnos(año, dias_restantes)

    return render_template('index.html', turnos=turnos)

def generar_turnos(año, dias_restantes):
    turnos = []
    fecha_actual = datetime(año, 1, 1)

    horarios = {
        1: {'inicio': '6:00 AM', 'fin': '2:00 PM'},
        2: {'inicio': '2:00 PM', 'fin': '10:00 PM'},
        3: {'inicio': '10:00 PM', 'fin': '6:00 AM'}
    }

    dias_descanso = {
        1: 1,
        2: 1,
        3: 1
    }

    while dias_restantes > 0:
        turno_actual = fecha_actual.hour // 8 + 1

        inicio = horarios[turno_actual]['inicio']
        fin = horarios[turno_actual]['fin']

        inicio_hora, inicio_minuto = obtener_hora_minuto(inicio)
        fin_hora, fin_minuto = obtener_hora_minuto(fin)

        inicio_turno = fecha_actual.replace(hour=inicio_hora, minute=inicio_minuto)
        fin_turno = fecha_actual.replace(hour=fin_hora, minute=fin_minuto)

        turno = {
            'inicio': inicio_turno,
            'fin': fin_turno,
            'descanso': fecha_actual + timedelta(days=6)
        }
        turnos.append(turno)

        dias_restantes -= 7 + dias_descanso[turno_actual]

        fecha_actual += timedelta(days=7 + dias_descanso[turno_actual])

    return turnos

def obtener_hora_minuto(cadena_hora):
    if ':' not in cadena_hora:
        raise ValueError('Formato de hora inválido: ' + cadena_hora)

    partes = cadena_hora.split(':')
    hora = int(partes[0])
    minuto = int(partes[1][:2])

    return hora, minuto

if __name__ == '__main__':
    app.run(debug=True)
