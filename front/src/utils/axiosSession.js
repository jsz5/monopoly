import axios from "axios";
import {getToken} from "./cookies"

axios.defaults.headers.common = {
    'Authorization': 'Token ' + getToken(),
    "Accept": "application/json",
    "Cookie": "csrftoken=" + getToken(),
};
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

export default axios;
