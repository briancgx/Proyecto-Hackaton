from flask import Flask, jsonify, request
from flask_cors import CORS
import mariadb
import sys
import random
import mysql.connector
app = Flask(__name__)
CORS(app, origins=["http://localhost:8080"])

# Configurar la conexión a MariaDB
config = {
    'host': '10.17.183.38',
    'port': 3306,
    'user': 'poncho',
    'password': 'poncho',
    'database': 'Hackaton'
}

@app.route('/login', methods=['POST'])
def login():
    credentials = request.json
    usuario = credentials.get('usuario')
    contrasena = credentials.get('contrasena')

    if not usuario or not contrasena:
        return jsonify({"message": "Usuario y contraseña son necesarios"}), 400

    try:
        conn = mariadb.connect(**config)
        cur = conn.cursor()
        
        # Cambia la consulta para seleccionar el ID_Profesor y el Nombre
        cur.execute("SELECT ID_Profesor, Nombre FROM Profesor WHERE Usuario = ? AND Contrasena = ?", (usuario, contrasena,))
        teacher = cur.fetchone()
        
        
        cur.execute("SELECT Nombre FROM Administrador WHERE Usuario = ? AND Contrasena = ?", (usuario, contrasena,))
        administrator = cur.fetchone()

        if teacher:
            profesor_id, teacher_name = teacher  # Desempaqueta correctamente el resultado de la consulta
            return jsonify({
                "message": "Login successful",
                "role": "Teacher",
                "name": teacher_name,
                "profesor_id": profesor_id
            }), 200
        elif administrator:
            # Obtener el nombre del administrador desde la consulta SQL
            admin_name = administrator[0]
            return jsonify({"message": "Login successful", "role": "Administrator", "name": admin_name}), 200
        else:
            return jsonify({"message": "Usuario o contraseña inválidos"}), 401

    except mariadb.Error as e:
        print(f"Error conectando a MariaDB: {e}")
        return jsonify({"message": "Error de conexión a la base de datos"}), 500
    finally:
        cur.close()
        conn.close()

                
@app.route('/api/data')
def get_api_data():
    # Mensaje de prueba para esta ruta
    return jsonify({"message": "Datos desde Flask por /api/data!"})

@app.route('/')
def get_root():
    try:
        # Conexión a la base de datos
        conn = mariadb.connect(**config)
        cur = conn.cursor()

        # Ejecución de una consulta SQL
        cur.execute("SELECT * FROM Administrador;")  # Asegúrate de que esta consulta sea relevante para tu base de datos
        rows = cur.fetchall()

        # Convertir los resultados en una lista de diccionarios
        results = []
        for row in rows:
            # Ajusta esto según la estructura de tu tabla
            results.append({"columna1": row[0], "columna2": row[1], "columna3": row[2]})

        cur.close()
        conn.close()

        return jsonify(results)
    except mariadb.Error as e:
        print(f"Error conectando a MariaDB: {e}")
        sys.exit(1)
        
@app.route('/api/asignaturas', methods=['GET'])
def get_asignaturas():
    try:
        conn = mariadb.connect(**config)
        cur = conn.cursor()

        cur.execute("SELECT Nombre FROM Asignatura;")
        asignaturas = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return jsonify([asignatura[0] for asignatura in asignaturas])
    except mariadb.Error as e:
        print(f"Error conectando a MariaDB: {e}")
        return jsonify({"message": "Error de conexión a la base de datos"}), 500

@app.route('/api/aulas', methods=['GET'])
def get_aulas():
    try:
        conn = mariadb.connect(**config)
        cur = conn.cursor()

        cur.execute("SELECT Nombre FROM Aula;")
        aulas = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return jsonify([aula[0] for aula in aulas])
    except mariadb.Error as e:
        print(f"Error conectando a MariaDB: {e}")
        return jsonify({"message": "Error de conexión a la base de datos"}), 500
    
@app.route('/api/disponibilidad', methods=['POST'])
def update_availability():
    data = request.json
    print("Received data:", data)  # Log the data to the console
    
    # Extracting 'profesor_id' from the received data
    profesor_id = data.get('profesor_id')
    if profesor_id is None:
        print("Error: 'profesor_id' is required.")
        return jsonify({"message": "'profesor_id' is required"}), 400
    
    # Attempt to convert 'profesor_id' to an integer
    try:
        profesor_id = int(profesor_id)
    except ValueError as e:
        print(f"Error converting 'profesor_id' to int: {e}")
        return jsonify({"message": "'profesor_id' must be an integer"}), 400
    
    # Extracting 'disponibilidad' and 'nombramiento' from the received data
    disponibilidad = data.get('disponibilidad')
    nombramiento = data.get('nombramiento')

    # Checking if 'disponibilidad' is a dictionary
    if not isinstance(disponibilidad, dict):
        print("Error: 'disponibilidad' must be a dictionary.")
        return jsonify({"message": "'disponibilidad' must be a dictionary"}), 400

    # Checking if 'nombramiento' is provided
    if nombramiento is None:
        print("Error: 'nombramiento' is None.")
        return jsonify({"message": "'nombramiento' is required"}), 400

    # Connecting to the database and updating availability
    try:
        conn = mariadb.connect(**config)
        cur = conn.cursor()

        # Deleting existing entries for the professor in the 'Disponibilidad' table
        delete_query = "DELETE FROM Disponibilidad WHERE profesor_id = ?"
        cur.execute(delete_query, (profesor_id,))

        # Inserting new availability data into the 'Disponibilidad' table
        for day, hours in disponibilidad.items():
            for hour_range in hours:
                start_time, end_time = hour_range.split(" - ")
                insert_query = """
                INSERT INTO Disponibilidad (profesor_id, dia, hora_inicio, hora_fin) 
                VALUES (?, ?, ?, ?)
                """
                cur.execute(insert_query, (profesor_id, day, start_time, end_time))
        
        # Updating 'nombramiento' if necessary (you need to update this with the correct table and column names)
        # Assuming that the 'nombramiento' column exists in a table that is related to 'profesor_id'
        update_nombramiento_query = """
        UPDATE Profesor 
        SET Horas_Nombramiento = ? 
        WHERE ID_Profesor = ?
        """
        cur.execute(update_nombramiento_query, (nombramiento, profesor_id))

        conn.commit()
        return jsonify({"message": "Disponibilidad y nombramiento actualizados correctamente"}), 200
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return jsonify({"message": "Database connection error"}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/actualizar_materias_aulas', methods=['POST'])
def actualizar_materias_aulas():
    data = request.json
    subjects = set(data.get('subjects', []))  # Usar un conjunto para eliminar duplicados
    classrooms = set(data.get('classrooms', []))

    try:
        conn = mariadb.connect(**config)
        cur = conn.cursor()

        # Actualizar materias
        # Seleccionar todas las materias existentes
        cur.execute("SELECT Nombre FROM Asignatura")
        existing_subjects = set(nombre for (nombre,) in cur.fetchall())
        
        # Calcular diferencias para saber qué añadir y qué eliminar
        subjects_to_add = subjects - existing_subjects
        subjects_to_remove = existing_subjects - subjects

        # Eliminar materias que ya no estén presentes
        for subject in subjects_to_remove:
            cur.execute("DELETE FROM Asignatura WHERE Nombre = ?", (subject,))
        
        # Añadir nuevas materias
        for subject in subjects_to_add:
            cur.execute("INSERT INTO Asignatura (Nombre) VALUES (?)", (subject,))

        # Actualizar aulas
        # Seleccionar todas las aulas existentes
        cur.execute("SELECT Nombre FROM Aula")
        existing_classrooms = set(nombre for (nombre,) in cur.fetchall())
        
        # Calcular diferencias para saber qué añadir y qué eliminar
        classrooms_to_add = classrooms - existing_classrooms
        classrooms_to_remove = existing_classrooms - classrooms

        # Eliminar aulas que ya no estén presentes
        for classroom in classrooms_to_remove:
            cur.execute("DELETE FROM Aula WHERE Nombre = ?", (classroom,))
        
        # Añadir nuevas aulas
        for classroom in classrooms_to_add:
            cur.execute("INSERT INTO Aula (Nombre) VALUES (?)", (classroom,))

        conn.commit()
        return jsonify({"message": "Materias y aulas actualizadas con éxito"}), 200
    except mariadb.Error as e:
        print(f"Error conectando a MariaDB: {e}")
        conn.rollback()
        return jsonify({"message": "Error de conexión a la base de datos"}), 500
    finally:
        cur.close()
        conn.close()



def obtener_profesores():
    conn = mariadb.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT ID_Profesor, Horas_Nombramiento FROM Profesor")
    profesores = {prof['ID_Profesor']: prof['Horas_Nombramiento'] for prof in cursor.fetchall()}
    cursor.close()
    conn.close()
    return profesores

def obtener_materias():
    conn = mariadb.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT Nombre, Creditos FROM Asignatura")
    materias = {mat['Nombre']: {'Horas_Semanales': mat['Creditos']} for mat in cursor.fetchall()}
    cursor.close()
    conn.close()
    return materias

def obtener_aulas():
    conn = mariadb.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT Nombre FROM Aula")
    aulas = [aula['Nombre'] for aula in cursor.fetchall()]
    cursor.close()
    conn.close()
    return aulas

def obtener_disponibilidad():
    conn = mariadb.connect(**config)
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

@app.route('/horario', methods=['GET'])
def obtener_horario():
    # Asumiendo que la función algoritmo_genetico ya está definida
    profesores = obtener_profesores()
    materias = obtener_materias()
    aulas = obtener_aulas()
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
    horarios = [f"{hora}:00" for hora in range(7, 21)]
    tamano_poblacion = 50
    numero_de_generaciones = 100
    
    mejor_solucion = algoritmo_genetico(materias, profesores, aulas, dias, horarios, tamano_poblacion, numero_de_generaciones)
    
    # Preparar la respuesta
    horario = [{
        'profesor': asignacion.profesor,
        'materia': asignacion.materia,
        'aula': asignacion.aula,
        'dia': asignacion.dia,
        'horario': asignacion.horario
    } for asignacion in mejor_solucion.asignaciones]
    
    return jsonify(horario)
if __name__ == '__main__':
    app.run(debug=True)
