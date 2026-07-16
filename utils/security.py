import bcrypt


def get_hashed_password(password: str) -> str:
    password_bytes = password.encode()[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode()