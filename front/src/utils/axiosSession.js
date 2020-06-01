import axios from "axios";
import {getToken} from "./cookies"

axios.defaults.headers.common = {
    'Authorization': 'Bearer ' + getToken(),
    "Accept": "application/json"
};

export default axios;
