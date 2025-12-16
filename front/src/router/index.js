import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import DevopsView from "../views/DevopsView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/devops",
    name: "devops",
    component: DevopsView,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
