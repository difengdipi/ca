
import Cookies from "js-cookie";

export async function getControlRoutes_url() {
    const user = JSON.parse(Cookies.get('user'));
    const role = user.role
    let url = ''
    if (role == null) {
        url = `/menus/admin-menu.json`
    }
    else if (role.role_name === '商户') {
        url = `/menus/merchant-menu.json`
    }
    else if (role.role_name === '顾客') {
        url = `/menus/customer-menu.json`
    }
    else {
        url = `/menus/user-menu.json`
    }
    return url
}