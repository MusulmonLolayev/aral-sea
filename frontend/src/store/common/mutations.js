export function setIsRefreshingTokenExpired(state, { status }) {
    state.IsRefreshingTokenExpired = status
}
export function setLangOptions(state) {
    state.LangOptions = [
        { value: 'en-us', label: this.lang.t('lang_en') },
        { value: 'uz', label: this.lang.t('lang_uz') }
    ]
    state.WellList_Colunms = [
        {
            name: "number",
            required: true,
            label: this.lang.t("number"),
            align: "left",
            field: "number",
            sortable: true,
        },
        {
            name: "x",
            align: "left",
            label: "X",
            field: "x",
            sortable: true,
        },
        {
            name: "y",
            align: "left",
            label: "Y",
            field: "y",
            sortable: true,
        },
        {
            name: "built_year",
            align: "left",
            label: this.lang.t('built_year'),
            field: "built_year",
            sortable: true,
        },
        {
            name: "depth",
            align: "left",
            label: this.lang.t('depth') + " (m)",
            field: "depth",
            sortable: true,
        },
        {
            name: "diameter",
            align: "left",
            label: this.lang.t('diameter') + " (m)",
            field: "diameter",
            sortable: true,
        },
        /*{
            name: "material",
            align: "material",
            label: this.lang.t('material'),
            field: "material",
            sortable: true,
        },*/
        {
            name: "area",
            align: "area",
            label: this.lang.t('area') + " (m)",
            field: "area",
            sortable: true,
        },
        {
            name: "label",
            align: "label",
            label: this.lang.t('label'),
            field: "label",
            sortable: true,
        },
        /*{
            name: "farm",
            align: "farm",
            label: this.lang.t('farm'),
            field: "farm",
            sortable: true,
        },*/
    ]
}
export function setConnectionStatus(state, { status }) {
    state.IsOnline = status
}