export function setIsRefreshingTokenExpired(state, { status }) {
    state.IsRefreshingTokenExpired = status
}
export function setLangOptions(state) {
    state.LangOptions = [
        { value: 'en-us', label: this.lang.t('lang_en').format_letter() },
        { value: 'uz', label: this.lang.t('lang_uz').format_letter() }
    ]
    state.WellList_Colunms = [
        {
            name: "number",
            required: true,
            label: this.lang.t("number").format_letter(),
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
            label: this.lang.t('built_year').format_letter(),
            field: "built_year",
            sortable: true,
        },
        {
            name: "depth",
            align: "left",
            label: this.lang.t('depth').format_letter() + " (m)",
            field: "depth",
            sortable: true,
        },
        {
            name: "diameter",
            align: "left",
            label: this.lang.t('diameter').format_letter() + " (m)",
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
            label: this.lang.t('area').format_letter() + " (m)",
            field: "area",
            sortable: true,
        },
        {
            name: "label",
            align: "label",
            label: this.lang.t('label').format_letter(),
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
    ],
    state.StaffList_Colunms = [
        {
            name: "last_name",
            required: true,
            label: this.lang.t("last_name").format_letter(),
            align: "left",
            field: "last_name",
            sortable: true,
        },
        {
            name: "first_name",
            required: true,
            label: this.lang.t("first_name").format_letter(),
            align: "left",
            field: "first_name",
            sortable: true,
        },
        {
            name: "middle_name",
            required: true,
            label: this.lang.t("middle_name").format_letter(),
            align: "left",
            field: "middle_name",
            sortable: true,
        },
        {
            name: "position_name",
            required: true,
            label: this.lang.t("position").format_letter(),
            align: "left",
            field: "position_name",
            sortable: true,
        },
    ]
}
export function setConnectionStatus(state, { status }) {
    state.IsOnline = status
}