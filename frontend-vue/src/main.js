import App from "./App.vue";

import Vue from "vue";

// Load view router
import VueRouter from "vue-router";
Vue.use(VueRouter);

// Load AXIOS
import axios from "axios";
import VueAxios from "vue-axios";
Vue.use(VueAxios, axios);

// Load Boostrap
import { BootstrapVue, IconsPlugin } from "bootstrap-vue";

// Make BootstrapVue available throughout your project
Vue.use(BootstrapVue);

// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin);
Vue.config.productionTip = false;

// Import Bootstrap an BootstrapVue CSS files (order is important)
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

// Define routes
const routes = [
  { path: "/books", component: () => import("./pages/BookProjector.vue") },
  {
    path: "/chapters",
    component: () => import("./pages/ChapterProjector.vue"),
  },
  { path: "/", component: () => import("./pages/HomePage.vue") },
  { path: "/about", component: () => import("./pages/About.vue") },
];
// Create router
const router = new VueRouter({
  mode: "history",
  routes,
});

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
