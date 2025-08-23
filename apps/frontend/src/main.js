import { createApp } from 'vue';
import App from './App.vue';
import PresentedBy from './components/PresentedBy.vue';
import './assets/styles.css';

const app = createApp(App);
app.component('PresentedBy', PresentedBy);
app.mount('#app');
