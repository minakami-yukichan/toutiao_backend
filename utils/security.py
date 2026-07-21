import hashlib
import bcrypt

def _truncate_password(password: str) -> bytes:
    return hashlib.sha256(password.encode()).hexdigest().encode()

def get_hashed_password(password: str) -> str:
    return bcrypt.hashpw(_truncate_password(password), bcrypt.gensalt()).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(_truncate_password(plain_password), hashed_password.encode())
