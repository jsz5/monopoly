import axios from "axios";
import {getToken, setToken} from "./cookies"

axios.defaults.headers.common = {
    'Authorization': 'Bearer ' + getToken()
};

export default axios;
