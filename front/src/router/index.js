import Vue from "vue";
import VueRouter from "vue-router";
import Login from "../views/Login.vue";
import PageNotFound from "../views/PageNotFound";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Login",
    component: Login
  },
  {
    path: "/start-game",
    name: "Zacznij Grę",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/StartGame.vue")
  },
  {
    path: "/board",
    name: "Board",
    component: () => import("../views/Board.vue")
  },
  {
    path: '*',
    component: PageNotFound
  },
];

const router = new VueRouter({
  routes
});

export default router;
