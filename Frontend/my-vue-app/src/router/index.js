import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import AdminDashboard from '../views/AdminDashboard.vue';
import TeacherDashboard from '../views/TeacherDashboard.vue';


// Función para comprobar si el usuario está autenticado
const isAuthenticated = () => {
  // Aquí deberías implementar tu lógica para comprobar si el usuario está autenticado
  // Por ejemplo, comprobar si existe un token en el almacenamiento local:
  return localStorage.getItem('authToken');
};

// Función para obtener el rol del usuario autenticado
const getUserRole = () => {
  // Aquí deberías implementar tu lógica para obtener el rol del usuario
  // Por ejemplo, obtener el rol almacenado en el almacenamiento local:
  return localStorage.getItem('userRole');
};

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/admin-dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, role: 'Administrator' }
  },
  {
    path: '/teacher-dashboard',
    name: 'TeacherDashboard',
    component: TeacherDashboard,
    meta: { requiresAuth: true, role: 'Teacher' }
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  const requiresAuth = to.meta.requiresAuth;
  const role = to.meta.role;
  const roleOfUser = getUserRole();

  if (requiresAuth && !isAuthenticated()) {
    // Si la ruta requiere autenticación y el usuario no está autenticado, redirige a Login
    next({ name: 'Login' });
  } else if (requiresAuth && role && roleOfUser !== role) {
    // Si la ruta requiere un rol específico y el usuario no tiene ese rol, redirige a Home o muestra un mensaje de error
    // Puedes mostrar un mensaje de error o redirigir a una página de error
    alert('No tienes permiso para acceder a esta página.');
    next({ name: 'Home' });
  } else {
    // Si no hay restricciones de autenticación o el usuario cumple con los requisitos, permite la navegación
    next();
  }
});

export default router;
