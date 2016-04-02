def checkUsername(username):
    #username length between 4 and 16
    #username must have at least 1 number and 1 letter
    if not 4 < len(username) < 16 or not username.isalnum():
        return False
    return True

def checkPassword(password):
    #password length between 8 and 32
    #password must have at least 1 number and 1 letter
    #password cannot contain symbols
    if not 8 <= len(password) <= 32 or not password.isalnum() or password.isalpha() or password.isnumeric():
        return False
    return True

def checkEmail(email):
    #must look like an email. If they don't get email it is because they entered wrong.
    if '@' not in email:
        return False
    uname, domain = email.split('@')
    if '.' not in domain:
        return False
    domain, ext = domain.split('.')
    if len(domain) < 2 or len(ext) <= 1:
        return False
    return True
