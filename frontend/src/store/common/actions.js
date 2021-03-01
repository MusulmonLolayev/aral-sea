import { Notify } from 'quasar'
import { Dialog } from 'quasar'

export function setIsRefreshingTokenExpired(context, { status }) {
    context.commit('setIsRefreshingTokenExpired', { status: status })
}
export function setLangOptions(context) {
    context.commit('setLangOptions')
}
export function setConnectionStatus(context, { status }) {
    context.commit('setConnectionStatus', { status: status })
}

export function no_internet_notify(context) {
    Notify.create({
        message: this.lang.t('no_internet_connection'),
        color: "red",
        icon: "error",
        actions: [{ label: this.lang.t("close"), color: "white" }],
    })
}

export function internal_server_error_dialog(context) {
    Dialog.create({
        title: null,
        message: this.lang.t('internal_server_error'),
        ok: true,
        persistent: true,
    })
}