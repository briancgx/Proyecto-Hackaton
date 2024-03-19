import mysql.connector
import random

# Conexión a la base de datos
def conectar_db():
    return mysql.connector.connect(
        host="10.17.183.38",
        user="poncho",
        password="poncho",
        database="Hackaton"
    )

# Obtención de datos de la base de datos
def obtener_profesores():
    conn = conectar_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT ID_Profesor, Horas_Nombramiento FROM Profesor")
    profesores = {prof['ID_Profesor']: prof['Horas_Nombramiento'] for prof in cursor.fetchall()}
    cursor.close()
    conn.close()
    return profesores

def obtener_materias():
    conn = conectar_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT Nombre, Creditos FROM Asignatura")
    materias = {mat['Nombre']: {'Horas_Semanales': mat['Creditos']} for mat in cursor.fetchall()}
    cursor.close()
    conn.close()
    return materias

def obtener_aulas():
    conn = conectar_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT Nombre FROM Aula")
    aulas = [aula['Nombre'] for aula in cursor.fetchall()]
    cursor.close()
    conn.close()
    return aulas

def obtener_disponibilidad():
    conn = conectar_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Disponibilidad")
    disponibilidad = {}
    for disp in cursor.fetchall():
        if disp['profesor_id'] not in disponibilidad:
            disponibilidad[disp['profesor_id']] = []
        disponibilidad[disp['profesor_id']].append((disp['dia'], disp['hora_inicio'], disp['hora_fin']))
    cursor.close()
    conn.close()
    return disponibilidad

# Definición de clases y funciones del algoritmo genético
class Asignacion:
    def __init__(self, profesor, materia, aula, dia, horario):
        self.profesor = profesor
        self.materia = materia
        self.aula = aula
        self.dia = dia
        self.horario = horario

class Solucion:
    def __init__(self, asignaciones):
        self.asignaciones = asignaciones
        self.fitness = self.calcular_fitness()

    def calcular_fitness(self):
        choques_maestro = 0
        choques_aula = 0
        for i, asignacion1 in enumerate(self.asignaciones):
            for asignacion2 in self.asignaciones[i+1:]:
                if asignacion1.profesor == asignacion2.profesor and asignacion1.dia == asignacion2.dia and asignacion1.horario == asignacion2.horario:
                    choques_maestro += 1
                if asignacion1.aula == asignacion2.aula and asignacion1.dia == asignacion2.dia and asignacion1.horario == asignacion2.horario:
                    choques_aula += 1
        total_choques = choques_maestro + choques_aula
        return 1 / (1 + total_choques)

def generar_asignaciones(materias, profesores, aulas, dias, horarios):
    asignaciones = []
    for materia, info in materias.items():
        for _ in range(info['Horas_Semanales']):
            profesor = random.choice(list(profesores.keys()))  # Asignación aleatoria de profesores
            dia = random.choice(dias)
            horario = random.choice(horarios)
            aula = random.choice(aulas)
            asignaciones.append(Asignacion(profesor, materia, aula, dia, horario))
    return asignaciones

def generar_poblacion_inicial(materias, profesores, aulas, dias, horarios, tamano_poblacion):
    poblacion = []
    for _ in range(tamano_poblacion):
        asignaciones = generar_asignaciones(materias, profesores, aulas, dias, horarios)
        poblacion.append(Solucion(asignaciones))
    return poblacion

def seleccionar_padres(poblacion):
    return sorted(poblacion, key=lambda x: x.fitness, reverse=True)[:len(poblacion)//2]

def cruzar(padres):
    hijos = []
    # Asegurarse de iterar de dos en dos, pero sin pasarse del final de la lista
    for i in range(0, len(padres) - 1, 2):  # -1 asegura no pasarnos si es impar
        punto_cruce = random.randint(1, len(padres[i].asignaciones)-2)
        hijos_asignaciones1 = padres[i].asignaciones[:punto_cruce] + padres[i+1].asignaciones[punto_cruce:]
        hijos_asignaciones2 = padres[i+1].asignaciones[:punto_cruce] + padres[i].asignaciones[punto_cruce:]
        hijos.append(Solucion(hijos_asignaciones1))
        hijos.append(Solucion(hijos_asignaciones2))
    return hijos


def seleccionar_nueva_generacion(poblacion_actual, hijos):
    # Combinar la población actual con los nuevos hijos
    poblacion_combinada = poblacion_actual + hijos
    # Ordenar la población combinada por fitness de forma descendente (mayor fitness primero)
    poblacion_ordenada = sorted(poblacion_combinada, key=lambda x: x.fitness, reverse=True)
    # Seleccionar los individuos más aptos hasta alcanzar el tamaño de la población original
    nueva_generacion = poblacion_ordenada[:len(poblacion_actual)]
    return nueva_generacion


def mutar(solucion, materias, profesores, aulas, dias, horarios):
    indice_asignacion = random.randint(0, len(solucion.asignaciones) - 1)
    profesor = random.choice(list(profesores.keys()))  # Asignación aleatoria de profesores para mutación
    materia = random.choice(list(materias.keys()))
    dia = random.choice(dias)
    horario = random.choice(horarios)
    aula = random.choice(aulas)
    solucion.asignaciones[indice_asignacion] = Asignacion(profesor, materia, aula, dia, horario)
    solucion.fitness = solucion.calcular_fitness()
    return solucion

def algoritmo_genetico(materias, profesores, aulas, dias, horarios, tamano_poblacion, numero_de_generaciones):
    poblacion = generar_poblacion_inicial(materias, profesores, aulas, dias, horarios, tamano_poblacion)
    for _ in range(numero_de_generaciones):
        padres = seleccionar_padres(poblacion)
        hijos = cruzar(padres)
        for hijo in hijos:
            if random.random() < 0.1:  # Probabilidad de mutación
                mutar(hijo, materias, profesores, aulas, dias, horarios)
        poblacion = seleccionar_nueva_generacion(poblacion, hijos)
    return max(poblacion, key=lambda x: x.fitness)

# Parámetros de ejecución
profesores = obtener_profesores()
materias = obtener_materias()
aulas = obtener_aulas()
dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
horarios = [f"{hora}:00" for hora in range(7, 21)]
tamano_poblacion = 50
numero_de_generaciones = 100

# Ejecutar algoritmo genético
mejor_solucion = algoritmo_genetico(materias, profesores, aulas, dias, horarios, tamano_poblacion, numero_de_generaciones)

# Mostrar la mejor solución encontrada
print("Mejor solución encontrada:")
for asignacion in mejor_solucion.asignaciones:
    print(f"{asignacion.profesor} enseña {asignacion.materia} en {asignacion.aula} el {asignacion.dia} a las {asignacion.horario}")