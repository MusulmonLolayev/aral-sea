export default function () {
  return {
    IsLoggined: localStorage.getItem('access_token') || localStorage.getItem('refresh_token') ? true : false,
    access_token: localStorage.getItem('access_token'),
    refresh_token: localStorage.getItem('refresh_token'),  
  }
}
