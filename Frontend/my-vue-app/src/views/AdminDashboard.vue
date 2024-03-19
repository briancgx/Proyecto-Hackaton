<template>
    <div class="admin-dashboard">
    <!-- Contenido omitido para simplificar -->
    <button @click="downloadCSV">Descargar Horario (Excel)</button>
  </div>
  <div class="admin-dashboard">
    <h1 class="animated-element">Hola {{ userName }}</h1>
    <div class="header animated-element">
      <button @click="toggleScheduleChange">Cambiar Horario</button>
    </div>
    <div class="current-schedule animated-element" v-if="showCurrentSchedule">
      <h2>Horario Actual</h2>
      <div v-for="asignacion in horario" :key="asignacion.profesor + asignacion.dia + asignacion.horario" class="asignacion-item">
        {{ asignacion.dia }} {{ asignacion.horario }}: {{ asignacion.materia }} - {{ asignacion.profesor }} en {{ asignacion.aula }}
      </div>
    </div>
  </div>
  
      <!-- Transición para el modal -->
      <transition name="fade">
        <div class="schedule-change-modal" v-if="showModal">
          <div class="generator animated-element">
            <div class="subjects">
              <h2>Materias</h2>
              <select v-model="selectedSubject">
                <option disabled value="">Seleccione una materia</option>
                <option v-for="subject in subjectOptions" :key="subject" :value="subject">
                  {{ subject }}
                </option>
              </select>
              <button @click="addSubject">Añadir Materia</button>
              <ul>
                <li v-for="(subject, index) in addedSubjects" :key="index">{{ subject }}</li>
              </ul>
            </div>
            <div class="classrooms">
              <h2>Aulas</h2>
              <select v-model="selectedClassroom">
                <option disabled value="">Seleccione un aula</option>
                <option v-for="classroom in classroomOptions" :key="classroom" :value="classroom">
                  {{ classroom }}
                </option>
              </select>
              <button @click="addClassroom">Añadir Aula</button>
              <ul>
                <li v-for="(classroom, index) in addedClassrooms" :key="index">{{ classroom }}</li>
              </ul>
            </div>
            <button>
                <a href="http://localhost:8080/admin-dashboard" style="text-decoration: none; color: inherit;">GENERAR</a>
            </button>

          </div>
        </div>
      </transition>

  </template>
  
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'AdminDashboard',
    data() {
      return {
        showModal: false,
        showCurrentSchedule: true,
        selectedSubject: '',
        subjectOptions: [],
        addedSubjects: [],
        selectedClassroom: '',
        classroomOptions: [],
        addedClassrooms: [],
        horario: [],
      };
    },
    created() {
    this.fetchSubjects();
    this.fetchClassrooms();
    this.fetchHorario(); // Agrega esta línea
    },
    computed: {
  userName() {
    const userName = localStorage.getItem('userName');
    console.log('Valor de userName en localStorage:', userName);
    return userName || 'Usuario';
  }
},
    methods: {
        downloadCSV() {
    const csvContent = "data:text/csv;charset=utf-8," + [
      ["Día", "Hora", "Materia", "Id_Profesor", "Aula"],
      ...this.horario.map(asignacion => [
        asignacion.dia,
        asignacion.horario,
        asignacion.materia,
        asignacion.profesor,
        asignacion.aula
      ])
    ].map(row => row.join(",")).join("\n");

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "horario.csv");
    document.body.appendChild(link);
    link.click();
  
},
      toggleScheduleChange() {
        this.showModal = !this.showModal;
        this.showCurrentSchedule = !this.showCurrentSchedule;
      },fetchHorario() {
  axios.get('http://localhost:5000/horario')
    .then(response => {
      console.log(response.data); // Log para depuración
      this.horario = response.data; // Asigna los datos a la propiedad horario
    })
    .catch(error => console.error('Hubo un error al obtener el horario:', error));
},

      fetchSubjects() {
        axios.get('http://localhost:5000/api/asignaturas') // Asegúrate de usar la URL completa.
          .then(response => {
            this.subjectOptions = response.data; // Asignación directa de la respuesta de la API
          })
          .catch(error => {
            console.error('Error al cargar las materias:', error);
          });
      },
      fetchClassrooms() {
        axios.get('http://localhost:5000/api/aulas') // Asegúrate de usar la URL completa.
          .then(response => {
            this.classroomOptions = response.data; // Asignación directa de la respuesta de la API
          })
          .catch(error => {
            console.error('Error al cargar las aulas:', error);
          });
      },
      addSubject() {
        if (this.selectedSubject && !this.addedSubjects.includes(this.selectedSubject)) {
          this.addedSubjects.push(this.selectedSubject);
          this.selectedSubject = ''; // Resetear el valor seleccionado
        }
      },
      addClassroom() {
        if (this.selectedClassroom && !this.addedClassrooms.includes(this.selectedClassroom)) {
          this.addedClassrooms.push(this.selectedClassroom);
          this.selectedClassroom = ''; // Resetear el valor seleccionado
        }
      },
      generateSchedule() {
        // Implementa aquí la lógica para manejar la generación del horario con las materias y aulas agregadas
        console.log('Materias agregadas:', this.addedSubjects);
        console.log('Aulas agregadas:', this.addedClassrooms);
        // Aquí podrías hacer una petición POST para enviar los datos al servidor y procesar el horario
      },
    }
  }
  </script>

<style scoped>
/* Estilos para la animación de entrada */
.animated-element {
  animation: fadeIn 1.5s ease forwards;
  opacity: 0;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-50px); /* Mover el elemento hacia arriba al inicio de la animación */
  }
  to {
    opacity: 1;
    transform: translateY(0); /* Llevar el elemento a su posición original al final de la animación */
  }
}

/* Estilos adicionales */
.admin-dashboard {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #6be5ee 0%, #4754a3 100%); /* Fondo gradiente */
  color: #333;
  padding: 20px;
}

.header button {
  padding: 10px;
  margin-bottom: 20px;
  border-radius: 20px; /* Bordes más redondeados */
}

.current-schedule {
  background-color: white;
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 20px; /* Bordes más redondeados */
}

.schedule-change-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  padding: 20px;
  border: 1px solid #ccc;
  z-index: 10;
  border-radius: 20px; /* Bordes más redondeados */
}

.generator {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.subjects, .classrooms {
  margin: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  background-color: #6be5ee; /* Color similar al azul degradado */
  border-radius: 20px; /* Bordes más redondeados */
}

.subject, .classroom {
  margin-bottom: 5px;
}

select {
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: white;
  font-size: 16px;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 20px; /* Bordes más redondeados */
  background-color: #333;
  color: white;
  font-size: 16px;
  cursor: pointer;
}

button:hover {
  background-color: #64b8fd;
}
</style>