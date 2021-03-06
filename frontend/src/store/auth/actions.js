export function login(context, { access_token, refresh_token }) {
  context.commit("login_success", {
    access_token: access_token,
    refresh_token: refresh_token
  });
}

export function refresh_token(context, { access }) {
  this.$axios.defaults.headers.common["Authorization"] = `Bearer ${access}`;
  context.commit("refresh_token", { access_token: access });
}

export function logout(context) {
  context.commit("logout");
  return Promise.resolve();
}

export function user_role(context, { user_role }) {
  context.commit("user_role", { user_role: user_role });
}

export function user_information(context, { user_information }) {
  context.commit("user_information", {
    user_information: user_information
  });
}
