<template>
  <div class="login-container">
    <div class="login-form" ref="loginForm">
      <img :src="logoPath" alt="Logo" class="logo fade-in-element"/> <!-- Logo dentro del formulario -->
      <h2 :class="{ 'fade-in-element': animated }">Login</h2>
      <form @submit.prevent="login" :class="{ 'fade-in-element': animated }">
        <div class="form-group">
          <input type="text" v-model="username" placeholder="User" required :class="{ 'fade-in-element': animated }"/>
        </div>
        <div class="form-group">
          <input type="password" v-model="password" placeholder="Password" required :class="{ 'fade-in-element': animated }"/>
        </div>
        <div class="form-group">
          <button type="submit" :class="{ 'fade-in-element': animated }">LOGIN</button>
        </div>
        <a href="#" class="forgot-password" :class="{ 'fade-in-element': animated }">Forgot password?</a>
      </form>
    </div>
  </div>
</template>
  


<script>
import axios from 'axios';
// Importa la imagen desde tus assets
import logoPath from '@/images/logo.png';

export default {
  name: 'LoginComponent',
  data() {
    return {
      username: '',
      password: '',
      logoPath, // Esto hace que la imagen esté disponible en la plantilla
      animated: false // Variable para controlar la animación
      
    };
  },
  methods: {
    async login() {
  try {
    const response = await axios.post('http://localhost:5000/login', {
      usuario: this.username,
      contrasena: this.password
    });
    console.log("Respuesta completa:", response);
    console.log("Mensaje recibido:", response.data.message);

    if (response.data.message.includes('Login successful')) {
      localStorage.setItem('profesor_id', response.data.profesor_id);
    console.log('Nombre de usuario recibido:', response.data.name);
    localStorage.setItem('userRole', response.data.role);
    localStorage.setItem('userName', response.data.name); // Guarda el nombre del usuario

  if (response.data.role === 'Teacher') {
    this.$router.push('/teacher-dashboard');
  } else if (response.data.role === 'Administrator') {
    this.$router.push('/admin-dashboard');
  }
} else {
  alert('Invalid username or password!');
}

  } catch (error) {
    console.error('Error during login:', error);
    alert('Error during login. Please try again.');
  }
}
  },
  mounted() {
    // Iniciar la animación cuando el componente se monte en el DOM
    this.animated = true;
  }
}
</script>

<style scoped>
/* Estilos para la animación de entrada */
.fade-in-element {
  animation: fadeIn 1.5s ease forwards;
  opacity: 0;
}

@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: translateY(50px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Estilos para el contenedor y el formulario */
.login-container {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #6be5ee 0%, #4754a3 100%); /* Fondo gradiente */
}

.login-form {
  z-index: 1;
  padding: 2em;
  background: #FFFFFF;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border-radius: 30px;
  text-align: center;
  width: 300px; /* Ancho fijo del formulario */
}


.login-form h2 {
  margin-bottom: 0.5em;
  font-family: 'Montserrat', sans-serif;
}
.login-form p {
  margin-bottom: 1.5em;
  color: #607D8B;
  font-size: 0.9em;
}

.form-group {
  margin-bottom: 1em;
}

.form-group input {
  width: calc(100% - 20px);
  padding: 10px;
  border: none;
  border-bottom: 1px solid #B0BEC5;
  transition: border-color 0.3s;
}

.form-group input:focus {
  outline: none;
  border-bottom: 1px solid #2196F3;
}

button {
  width: 100%;
  padding: 10px;
  background: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background: #1E88E5;
}

a {
  text-decoration: none;
  color: #2196F3;
  transition: color 0.3s;
}

a:hover {
  color: #1E88E5;
}

.forgot-password {
  display: block;
  margin-top: 1em;
  margin-bottom: 0.5em;
  font-family: 'Nunito', sans-serif;

}

/* Estilos para el logo */
.logo {
  max-width: 140px; /* Tamaño del logo */
  margin-bottom: 20px; /* Espacio debajo del logo */
  margin-left: 25px; /* Espacio a la derecha del logo */
}

</style>