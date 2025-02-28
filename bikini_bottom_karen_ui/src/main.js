import { createApp } from 'vue'
import App from './App.vue'
import router from "@/router/index.js";
import '@fortawesome/fontawesome-free/css/all.css';


const app = createApp(App)

// 禁用 Vue DevTools
app.config.devtools = false
app.use(router)
app.mount('#app')
