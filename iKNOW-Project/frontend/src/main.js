// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import VueResource from 'vue-resource'
import iView from 'iview'
import 'iview/dist/styles/iview.css'
import globalValue from './components/globalValue'

// import Vuex from 'vuex'
Vue.prototype.GLOBAL = globalValue
Vue.config.productionTip = false

Vue.use(VueResource)
Vue.use(iView)
// Vue.use(Vuex)

// 取 cookie
function getCookie (name) {
  let reg = new RegExp('(^| )' + name + '=([^;]*)(;|$)')
  let arr
  if ((arr = document.cookie.match(reg))) {
    return decodeURIComponent(arr[2])
  }
}

// 设置 POST 请求时 的 data 格式
Vue.http.options.emulateJSON = true

// 设置 X-CSRFToken
Vue.http.interceptors.push(function (request, next) {
  // request.method = 'POST'
  request.headers.set('X-CSRFToken', getCookie('csrftoken'))
  next()
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})
