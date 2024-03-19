<template>
    <div class="teacher-dashboard fade-in-element">
      <h1 class="title">Hola Profe {{ userName }}</h1>
      <div class="toolbar">
        <!-- Iconos de toolbar aquí -->
      </div>
      <div class="nombramiento">
        <label for="nombramiento-input">Nombramiento:</label>
        <input type="number" id="nombramiento-input" v-model.number="nombramiento" min="4" max="40" @input="validateNombramiento">
      </div>
      <div class="availability">
        <h2>Horas disponibles</h2>
        <div class="calendar">
          <div class="days">
            <div>Lunes</div>
            <div>Martes</div>
            <div>Miércoles</div>
            <div>Jueves</div>
            <div>Viernes</div>
          </div>
          <div class="hours">
            <div v-for="hour in hours" :key="hour" class="hour-row">
              <div>{{ hour }}</div>
              <div class="hour-selection" v-for="day in days" :key="day"
                   :class="{'selected': isSelected(hour, day)}"
                   @click="toggleHour(day, hour)">
              </div>
            </div>
          </div>
        </div>
        <button @click="submitAvailability">Enviar</button>
      </div>
    </div>
  </template>
  
    <script>
  import axios from 'axios'; // Importa Axios para hacer solicitudes HTTP
  
  export default {
    name: 'TeacherDashboard',
    data() {
      return {
        nombramiento: null,
        hours: [
          '07:00 - 08:00 hrs', '08:00 - 09:00 hrs', '09:00 - 10:00 hrs',
          '10:00 - 11:00 hrs', '11:00 - 12:00 hrs', '12:00 - 13:00 hrs',
          '13:00 - 14:00 hrs', '14:00 - 15:00 hrs', '15:00 - 16:00 hrs',
          '16:00 - 17:00 hrs', '17:00 - 18:00 hrs', '18:00 - 19:00 hrs',
          '19:00 - 20:00 hrs', '20:00 - 21:00 hrs'
        ],
        days: ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes'],
        selectedHours: {}
      };
    },
    computed: {
      userName() {
        const userName = localStorage.getItem('userName');
        console.log('Valor de userName en localStorage:', userName);
        return userName || 'Usuario';
      }
    },
    methods: {
      validateNombramiento() {
        if (this.nombramiento < 4 || this.nombramiento > 40) {
          this.nombramiento = '';
        }
      },
      toggleHour(day, hour) {
        this.selectedHours[day] = this.selectedHours[day] || [];
        const index = this.selectedHours[day].indexOf(hour);
        if (index === -1) {
          this.selectedHours[day].push(hour);
        } else {
          this.selectedHours[day].splice(index, 1);
        }
      },
      isSelected(hour, day) {
        return this.selectedHours[day] && this.selectedHours[day].includes(hour);
      },
      calculateMinimumSelection() {
        if (this.nombramiento >= 4 && this.nombramiento <= 19) {
          return this.nombramiento;
        } else if (this.nombramiento >= 20 && this.nombramiento <= 40) {
          return Math.floor(this.nombramiento / 2) + 2;
        }
        return 0; // Default case, should not happen
      },
      isSelectionValid() {
        const totalSelected = Object.values(this.selectedHours).reduce((acc, curr) => acc + curr.length, 0);
        const minimumSelection = this.calculateMinimumSelection();
        return totalSelected >= minimumSelection;
      },
      async submitAvailability() {
        if (!this.isSelectionValid()) {
          alert(`Debes seleccionar al menos ${this.calculateMinimumSelection()} horas.`);
          return;
        }
  
        const profesor_id = localStorage.getItem('profesor_id');
        const formattedHours = this.formatSelectedHours();
        const data = {
          profesor_id: profesor_id,
          disponibilidad: formattedHours,
          nombramiento: this.nombramiento
        };
  
        try {
          const response = await axios.post('http://localhost:5000/api/disponibilidad', data);
          console.log(response.data.message);
          // Reset selected hours and appointment after successful submission
          this.selectedHours = {}; // Clears all selections
          this.nombramiento = null; // Resets the appointment to null or your initial value
        } catch (error) {
          console.error('Error al enviar disponibilidad:', error);
        }
      },
      formatSelectedHours() {
        const formattedHours = {};
        for (const day in this.selectedHours) {
          formattedHours[day] = this.selectedHours[day].map(hourRange => {
            const [start, end] = hourRange.split(' - ');
            return `${start}:00 - ${end.split(' ')[0]}:00`;
          });
        }
        return formattedHours;
      }
    }
  }
  </script>
    
  <style scoped>
  /* Animación de entrada para el dashboard del profesor */
  .teacher-dashboard {
    animation: fadeIn 1.5s ease forwards;
    opacity: 0;
  }
  
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(-50px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  /* Estilos generales */
  .teacher-dashboard {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #6be5ee 0%, #4754a3 100%);
    color: #333;
    padding: 20px;
  }
  
  /* Herramientas y otros controles */
  .teacher-dashboard .toolbar, .nombramiento, .availability, .calendar .days div, .calendar .hours .hour-row > div {
    border-radius: 20px;
  }
  
  .toolbar {
    display: flex;
    justify-content: space-around;
    padding: 10px;
  }
  
  .nombramiento, .availability {
    margin: 10px;
  }
  
  .nombramiento label, .nombramiento input, .availability button, .calendar .days div, .calendar .hours .hour-row > div {
    font-size: 16px;
  }
  
  .nombramiento input, .availability button {
    padding: 10px;
    margin-top: 10px;
    background-color: #ffff;
    color: black;
    border: none;
    cursor: pointer;
    border-radius: 20px;
  }
  
  .nombramiento input:focus, .availability button:hover {
    background-color: #64b8fd;
  }
  
  /* Calendario y selección de horas */
  .calendar .days {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    text-align: center;
    font-weight: bold;
  }
  
  .calendar .hours .hour-row {
    display: grid;
    grid-template-columns: auto repeat(5, 1fr);
    margin-bottom: 5px;
  }
  
  .hour-selection {
    height: 20px;
    background-color: #f0f0f0;
    border: 1px solid #e0e0e0;
    cursor: pointer;
  }
  
  .hour-selection.selected {
    background-color: #4CAF50;
  }
  
  /* Botones */
  .availability button {
    background-color: #474c51;
    color: white;
    border: none;
    cursor: pointer;
  }
  
  /* Ajustes finos a inputs y botones para coherencia */
  input[type="number"], button {
    border-radius: 4px;
  }
  
  input[type="number"]:focus {
    outline: none;
    border-color: #2196F3;
  }
  </style>
  