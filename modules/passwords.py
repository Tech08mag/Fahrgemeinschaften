import argon2
from argon2 import PasswordHasher

ph = PasswordHasher()

def hashing(password: str) -> str:
    hash = ph.hash(password)
    if ph.check_needs_rehash(hash):
      hash = ph.hash(password)
      return hash
    return hash

def verify(hashed_password, input: str) -> bool:
    try:
      ph.verify(hashed_password, input)
      return True
    except argon2.exceptions.VerifyMismatchError:
      return False