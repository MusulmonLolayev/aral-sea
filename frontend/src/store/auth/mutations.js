export function login_success(state, {access_token, refresh_token}){
    state.IsLoggined = true
    localStorage.setItem('access_token', access_token)
    state.access_token = access_token
    localStorage.setItem('refresh_token', refresh_token)
    state.refresh_token = refresh_token
}

export function refresh_token(state, {access_token}){
    localStorage.setItem('access_token', access_token)
    state.access_token = access_token
}

export function logout(state){
    state.IsLoggined = false
    state.access_token = ""
    state.refresh_token = ""
    localStorage.removeItem("access_token")
    localStorage.removeItem("refresh_token")
}
