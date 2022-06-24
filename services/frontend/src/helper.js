import { setCookies,getCookie, removeCookies } from 'cookies-next';

export function set_auth_token(token)
{
    setCookies('auth_token',token)

}

export function remove_auth_cookie()
{
    removeCookies('auth_token')
}

export function get_auth_token()
{
    const auth_token = getCookie("auth_token")

    return auth_token
}

// export async function is_user_logged_in()
// {
//     const token = get_auth_token()
//     if (auth_token == null || auth_token == undefined)
//     {
//         return null
//     }

//     return token
// }
