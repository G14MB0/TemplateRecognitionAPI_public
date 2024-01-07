#to hash passwords
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #crypt algo

def hash(password: str):
    return pwd_context.hash(password)


def verifyPassword(plain_pass, hash_pass):
    return pwd_context.verify(plain_pass, hash_pass)