export function setIsRefreshingTokenExpired(context, { status }) {
    context.commit('setIsRefreshingTokenExpired', { status: status })
}
export function setLangOptions(context) {
    context.commit('setLangOptions')
}
export function setConnectionStatus(context, { status }) {
    context.commit('setConnectionStatus', { status: status })
}