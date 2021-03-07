import { Api } from './axios'
import { i18n } from './i18n'
import { Notify } from 'quasar'
import { Dialog } from 'quasar'

String.prototype.format = function () {
  var formatted = this;
  for (var arg in arguments) {
    formatted = formatted.replace("{" + arg + "}", arguments[arg]);
  }
  return formatted;
};

Date.prototype.addMins = function(m) {     
  this.setTime(this.getTime() + (m*60*1000));  
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
      if (typeof instance.id == "undefined") {
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
      await Api.delete(url, {data: {'id': instance.id}})
      return true
    }
    catch (e) {
      return e
    }
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
        message: this.$t("edited"),
        color: "blue",
        icon: "success",
        actions: [{ label: this.$t("close"), color: "white" }],
      });
    } else {
      Notify.create({
        message: this.$t("unedited"),
        color: "red",
        icon: "error",
        actions: [{ label: this.$t("close"), color: "white" }],
      });
    }
  },
}

export default ({ store, Vue }) => {
  Vue.prototype.$helper = helper,
    store.$helper = helper
}

export {helper}