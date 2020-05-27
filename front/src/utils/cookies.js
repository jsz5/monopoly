const setCookie = (cname, cvalue, exdays = 30) => {
    let d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    let expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

const getCookie = (cname) => {
    let name = cname + "=";
    let ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

const TOKEN = "TOKEN"

const setToken = token => {
    setCookie(TOKEN, token);
}

const getToken = () => {
    return getCookie(TOKEN)
}

function checkToken() {
    let token = getCookie(TOKEN);
    if (token != "") {
        return true
    } else {
        return false
    }
}

const deleteToken = () => {
    document.cookie = TOKEN+'=; Max-Age=-99999999;';
}

export {getCookie, setCookie}
export {getToken, setToken}
export {checkToken}
export {deleteToken}