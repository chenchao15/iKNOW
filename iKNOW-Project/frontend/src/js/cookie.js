/*设置cookie 
  cookieArray = [{
    name: ,
    value: ,
    exdays: 
  }, ...]
*/
export function setCookie (cookieArray) {
    var exdate = new Date()
    for (var ckie in cookieArray) {
      exdate.setDate(exdate.getDate() + exdays)
      document.cookie = ckie.name + '=' + escape(ckie.value) + ';path=/' + ((ckie.exdays === null) ? '' : ';expires=' + exdate.toGMTString())
    }
}

/*获取cookie*/
export function getCookie(name){
    var ckie, reg = new RegExp('(^| )' + name + '=([^;]*)(;|$)')
    if ((ckie = document.cookie.match(reg)) {
      return unescape(ckie[2])
    } else {
      return null
    }
}

/*删除cookie*/
export function delCookie(name){
    setCookie([{name: name, value: '', exdays: -1}])
}