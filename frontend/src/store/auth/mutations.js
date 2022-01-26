export function login_success(state, { access_token, refresh_token }) {
  state.IsLoggined = true;
  localStorage.setItem("access_token", access_token);
  state.access_token = access_token;
  localStorage.setItem("refresh_token", refresh_token);
  state.refresh_token = refresh_token;
}

export function refresh_token(state, { access_token }) {
  localStorage.setItem("access_token", access_token);
  state.access_token = access_token;
}

export function logout(state) {
  state.IsLoggined = false;
  state.access_token = "";
  state.refresh_token = "";
    state.user_permissions = [];
    state.user_title = '';
    
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("user_title");
  localStorage.removeItem("user_permissions");
}

export function user_role(state, { user_role }) {
  localStorage.setItem("user_role", user_role);
  state.user_role = user_role;
}

export function user_information(state, { user_information }) {
  localStorage.setItem("user_permissions", user_information.permissions);
    state.user_permissions = user_information.permissions;
    
    localStorage.setItem("user_title", user_information.user_title);
    state.user_title = user_information.user_title;
}
