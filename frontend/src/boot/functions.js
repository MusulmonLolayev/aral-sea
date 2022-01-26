import { Api } from './axios'
import { i18n } from './i18n'
import { Notify } from 'quasar'

String.prototype.format = function () {
  var formatted = this;
  for (var arg in arguments) {
    formatted = formatted.replace("{" + arg + "}", arguments[arg]);
  }
  return formatted;
};

// format='Abs', the first letters of each word of the text drive to uppercase
// format='ABS', the all words of the text drive to uppercase
// format='abs', the first letters of each word of the text drive to lowercase
// format='abs', the all words of the text drive to lowercase: not done
String.prototype.format_letter = function (format='Abs') {
  var formatted = this;
  switch (format){
    case "abs": formatted = this.toLowerCase(); break;
    case "Abs": formatted = formatted.charAt(0).toUpperCase() + formatted.slice(1); break;
    case "ABS": formatted = formatted.toUpperCase(); break;
  }
  return formatted;
};

Date.prototype.addMins = function (m) {
  this.setTime(this.getTime() + (m * 60 * 1000));
  return this;
}

let helper = {
  lang(name) {
    return i18n.t(name)
  },

  message_types: {
    success: 'success',
    error: 'error'
  },


  rules: {
    select: [val => !!val],
    number: [val => !!val],
  },

  ToYesNO(value) {
    return value == true ? this.lang('yes') : this.lang('no');
  },
  ToBoolFromYesNo(value) {
    return value == this.lang('yes');
  },
  ToPlusMinus(value) {
    return value == true ? "+" : "-";
  },
  ToBoolFromPlusMinus(value) {
    return value == "+";
  },
  GetCurrentDate() {
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();

    today = yyyy + '-' + mm + '-' + dd;
    return today
  },

  async saveInstance(instance, url) {
    try {
      if (instance.id == 0) {
        let response = await Api
          .post(url, instance)
        instance.id = response.data
        return true
      } else {
        await Api
          .put(url, instance)
        return true
      }
    }
    catch (e) {
      return e
    }
  },

  async deleteInstance(instance, url) {
    try {
      await Api.delete(url, { data: { 'id': instance.id } })
      return true
    }
    catch (e) {
      return e
    }
  },

  async get_farm(farm_id){
    let response = await Api.get("farm_request/" + farm_id)
    return response.data[0]
  },

  async get_well(well_id){
    let response = await Api.get("well_request/" + well_id)
    return response.data
  },

  getSelectedString(numberOfRows) {
    return numberOfRows + " " + i18n.t("selected");
  },
  get_pagination_label(firstRowIndex, endRowIndex, totalRowsNumber) {
    return firstRowIndex + "-" + endRowIndex + " " + i18n.t("of") + " " + totalRowsNumber;
  },

  DealSavingRespone(response) {
    if (response == true) {
      Notify.create({
        message: this.lang("edited"),
        color: "blue",
        icon: "success",
        actions: [{ label: this.lang("close"), color: "white" }],
      });
    } else {
      Notify.create({
        message: this.lang("unedited"),
        color: "red",
        icon: "error",
        actions: [{ label: this.lang("close"), color: "white" }],
      });
    }
  },

  muster_pumping() {
    var d = new Date()
    let defaultItem = {
      id: 0,
      count_gall: 0,
      size_gall: 0,
      ugv_before_pumping: 0,
      ugv_after_pumping: 0,
      bottom: 0,
      speed_water: 0,
      elevated: 0,
      reduced: 0,
      date: helper.GetCurrentDate()
    }
    defaultItem.starting_pumping = d.toTimeString().substring(0, 8)
    d.addMins(10)
    defaultItem.finishing_pumping = d.toTimeString().substring(0, 8)
    return defaultItem
  },

  well() {
    let defaultItem = {
      id: 0,
      number: '1',
      x: 0,
      y: 0,
      built_year: 1980,
      depth: 0,
      speed_water: 0,
      diameter: 0,
      material: true,
      area: 0,
      label: 0,
    }
    return defaultItem
  },

  muster_soil(){
    return {
      id: 0,
      well: null,
      contour_no: null,
      pit_no: null,
      area_size: null,
      salt_degree: null,
      date: helper.GetCurrentDate(),
      crop_type: null,
      location_x: null,
      location_y: null,
    }
  },

  soil_deep(){
    return {
      id: 0,
      from_deep: 0,
      to_deep: 30,
      soil_type: null,
    }
  },

  ugv() {
    let defaultItem = {
      id: 0,
      degree: 0,
      date: helper.GetCurrentDate()
    }
    return defaultItem
  },

  soildeep() {
    let defaultItem = {
      id: 0,
      from_deep: 0,
      to_deep: 0,
      soiltype: null,
      mustersoil: null,
    }
    return defaultItem
  },

  farm(){
    return {
      id: 0,
      name: "",
      district: null,
    }
  }
}

export default ({ store, Vue }) => {
  Vue.prototype.$helper = helper,
    store.$helper = helper
}

export { helper }