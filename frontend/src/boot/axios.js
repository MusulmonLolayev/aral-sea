import axios from "axios";
import { Loading } from "quasar";
import { Notify } from "quasar";
import { Dialog } from "quasar";
import { helper } from "./functions";
import router from "src/router";

const baseURL = "http://127.0.0.1:8000/api";

const axiosConfig = {
  baseURL: baseURL,
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json"
  }
};

export const Api = axios.create(axiosConfig);

function refreshToken(store) {
  const refreshingCall = Api.post("/login/refresh", {
    refresh: store.state.auth.refresh_token
  })
    .then(response => {
      store.dispatch("auth/refresh_token", {
        access: response.data.access
      });
      store.dispatch("common/setIsRefreshingTokenExpired", { status: false });
      return Promise.resolve(true);
    })
    .catch(() => {
      return Promise.reject();
    });
  return refreshingCall;
}

let Is_Refreshed_Token = false;

let Is_Any_Error = false;
let Attempts_Count = 0;

export default ({ store, Vue, router }) => {
  (Api.defaults.headers.common[
    "Authorization"
  ] = `Bearer ${store.state.auth.access_token}`),
    (Vue.prototype.$axios = Api),
    (store.$axios = Api),
    Api.interceptors.request.use(
      function(request) {
        /*if (Is_Any_Error)
        return Promise.reject(request)*/
        // Fisrt must to check the internet connection
        /*if (!store.state.common.IsOnline && Attempts_Count == 0) {
        Dialog.create({
          title: helper.lang('error_in_connection'),
          message: helper.lang('no_internet_connection'),
          ok: helper.lang('ok'),
          persistent: true
        })
        Attempts_Count++
        return Promise.reject(request)
      }*/
        Loading.show();
        return Promise.resolve(request);
      },
      function(error) {
        Loading.hide();
        return Promise.reject(error);
      }
    ),
    Api.interceptors.response.use(
      function(response) {
        Loading.hide();
        return Promise.resolve(response);
      },
      function(error) {
        Loading.hide();
        Is_Any_Error = true;
        let data = error.response.data;

        // see https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
        switch (error.response.status) {
          // Bad request
          case 400:
            {
              Dialog.create({
                title: helper.lang("error_in_request"),
                message: helper.lang("error_in_data"),
                ok: helper.lang("ok"),
                persistent: true
              });
            }
            break;
          // Unauthorized
          case 401:
            {
              // tring to refresh the token
              if (
                !Is_Refreshed_Token &&
                data &&
                data.code &&
                data.code == "token_not_valid" &&
                store.state.auth.refresh_token
              ) {
                Is_Refreshed_Token = true;
                return refreshToken(store)
                  .then(_ => {
                    error.config.headers["Authorization"] =
                      "Bearer " + store.state.auth.access_token;
                    error.config.baseURL = undefined;
                    return Api.request(error.config);
                  })
                  .catch(error => {
                    return Promise.reject(error);
                  });
              } else {
                // If the refresh token is experid too, then the user must relogin
                if (Is_Refreshed_Token) {
                  store.dispatch("common/setIsRefreshingTokenExpired", {
                    status: true
                  });
                  router.push("/login");
                  return Promise.reject(error);
                } else {
                  // if there is the token is experid, then must the refresh the token
                  if (error.response.status === 401) {
                    router.push("/login");
                    return Promise.reject(error);
                  }
                }
              }
            }
            break;

          // 402 Payment Required
          case 402:
            {
              // must to do
            }
            break;

          // 403 Forbidden
          case 403:
            {
              console.log("ssss");
              // just the necessary permissions are dealed
              Dialog.create({
                title: helper.lang("error_in_permission"),
                message:
                  helper.lang("not_permission") +
                  ", " +
                  helper.lang("please_relogin"),
                ok: helper.lang("ok"),
                persistent: true
              }).onOk(() => {
                return Promise.reject(error);
              });
            }
            break;

          // 404 source not found
          case 404:
            {
              router.push('/not-found-resource')
            }
            break;

          // Internal server errors
          case 500:
            {
              // just the necessary permissions are dealed
              Dialog.create({
                title: helper.lang("error_in_server"),
                message: helper.lang("internal_server_error"),
                ok: helper.lang("ok"),
                persistent: true
              });
            }
            break;
        }

        // Check Internal server error
        if (error.response.status === 500) {
        }
        return Promise.reject(error);
      }
    );
};
