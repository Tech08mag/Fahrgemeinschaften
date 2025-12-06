import os
import base64
from argon2 import PasswordHasher

ph = PasswordHasher()


def generate_salt(length: int = 16) -> str:
    return base64.b64encode(os.urandom(length)).decode('utf-8')

def hashing(password: str):
  salt: str = generate_salt()
  hash = ph.hash(password + salt)
  if ph.check_needs_rehash(hash):
    hash = ph.hash(password + salt)
    return hash
  return hash

def verify(hashed_password, input: str, salt):
  try:
      ph.verify(hashed_password, input + salt)
      return True
  except argon2.exceptions.VerifyMismatchError:
     return False