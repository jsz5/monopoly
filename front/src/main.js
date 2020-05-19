import Vue from 'vue'
// import App from './App.vue'
import VueRouter from 'vue-router'

// Vue.config.productionTip = false

Vue.use(VueRouter)

const Foo = { component: {
    template: "<div>Foo</div>"
  } }
const Bar = { component: {
    template: "<div>Bar</div>"
  } }
import Home from "./components/HelloWorld"

const routes = [
  { path: '/foo', component: Foo },
  { path: '/bar', component: Bar },
  { path: '/', component: Home}
]

const router = new VueRouter({
  routes // short for `routes: routes`
})

// render: h => h(App),
new Vue({
  router,
  template: `
    <div>
      <nav class="navbar navbar-toggleable-md navbar-light bg-faded">
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item"><router-link to="/" class="nav-link">Home</router-link></li>
            <li class="nav-item"><router-link to="/about" class="nav-link">About</router-link></li>
            <li class="nav-item"><router-link to="/contact" class="nav-link">Contact</router-link></li>
          </ul>
        </div>
      </nav>
      <router-view class="view"></router-view>
    </div>
  `
}).$mount('#app')
