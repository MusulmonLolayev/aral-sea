import axios from 'axios'
import { Loading } from 'quasar'

const baseURL = 'http://127.0.0.1:8000/api'

const axiosConfig = {
  baseURL: baseURL,
  headers: {
    Accept: "application/json", "Content-Type": "application/json"
  },
};

export const Api = axios.create(axiosConfig)

function refreshToken(store) {
  const refreshingCall = Api.post('/login/refresh', {
    refresh: store.state.auth.refresh_token
  })
    .then(response => {
      store.dispatch('auth/refresh_token',
        {
          access: response.data.access
        })
      store.dispatch('common/setIsRefreshingTokenExpired', { status: false })
      return Promise.resolve(true)
    })
    .catch(() => {
      return Promise.reject()
    })
  return refreshingCall
}

let Is_Refreshed_Token = false

export default ({ store, Vue, router }) => {
  Api.defaults.headers.common['Authorization'] = `Bearer ${store.state.auth.access_token}`,
    Vue.prototype.$axios = Api,
    store.$axios = Api,
    Api.interceptors.request.use(function (request) {
      // Fisrt must to check the internet connection
      if (!store.state.common.IsOnline) {
        store.dispatch('common/no_internet_notify')
        return Promise.reject(request)
      }
      Loading.show()
      return Promise.resolve(request)
    }, function(error) {
      Loading.hide()
      return Promise.reject(error)
    }),
    Api.interceptors.response.use(
      function (response) {
        Loading.hide()
        return Promise.resolve(response)
      },
      function (error) {
        Loading.hide()
        // Check error is Network error
        if (!error.response.status) {
          return Promise.reject(error)
        }

        // Check Internal server error
        if (error.response.status === 500) {
          store.dispatch('common/internal_server_error_dialog')
          return Promise.reject(error)
        }
        let data = error.response.data
        // if there is the token is experid, then must the refresh the token
        if (!Is_Refreshed_Token &&
          error.response.status === 401 &&
          data && data.code && data.code == "token_not_valid" &&
          store.state.auth.refresh_token) {
          Is_Refreshed_Token = true
          return refreshToken(store).then(_ => {
            error.config.headers['Authorization'] = 'Bearer ' + store.state.auth.access_token;
            error.config.baseURL = undefined;
            return Api.request(error.config);
          })
            .catch((error) => {
              return Promise.reject(error)
            })
        }
        else {
          // If the refresh token is experid too, then the user must relogin 
          if (Is_Refreshed_Token) {

            store.dispatch('common/setIsRefreshingTokenExpired', { status: true })
            router.push('/login')
          }
          else {

          }
        }
      }
    )
}