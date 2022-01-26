export default function() {
  let user_permissions = localStorage.getItem("user_permissions");
  if (user_permissions != null && user_permissions != "")
    user_permissions = user_permissions.split(",");
  else user_permissions = [];
  return {
    IsLoggined:
      localStorage.getItem("access_token") ||
      localStorage.getItem("refresh_token")
        ? true
        : false,
    access_token: localStorage.getItem("access_token"),
    refresh_token: localStorage.getItem("refresh_token"),
    user_role: localStorage.getItem("user_role"),
    user_permissions: user_permissions,
    user_title: localStorage.getItem('user_title'),
  };
}
