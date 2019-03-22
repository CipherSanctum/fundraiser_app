# ADD ALL THESE TO YOUR SETTINGS.PY


PAYTRACE_API_USER_NAME = 'your_api_username'         # make an api user, because the password for it never expires, unlike the default one
PAYTRACE_API_USER_PASSWORD = 'the_password_for_it'
PAYTRACE_API_USER_INTEGRATOR_ID = 'abcde12345'       # you get this when you make a sandbox account
PAYTRACE_NEW_ACCESS_TOKEN_CREDENTIALS = {
    'grant_type': 'password',                        # leave this 'password' type alone
    'username': PAYTRACE_API_USER_NAME,
    'password': PAYTRACE_API_USER_PASSWORD,
    'integrator_id': PAYTRACE_API_USER_INTEGRATOR_ID,
}
PAYTRACE_NEW_ACCESS_TOKEN_HEADERS = {
    'Accept': '*/*',
    'HTTP Protocol': 'HTTP/1.1',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}
