// Importa la función createApp desde Vue
import { createApp } from 'vue';

// Importa el componente principal de la aplicación (App.vue)
import App from './App.vue';

// Importa el enrutador (router) de la aplicación
import router from './router';

// Crea una instancia de la aplicación Vue utilizando la función createApp
createApp(App)

  // Usa el enrutador (router) en la instancia de la aplicación
  .use(router)

  // Monta la aplicación en el elemento con el ID 'app' en el DOM
  .mount('#app');
