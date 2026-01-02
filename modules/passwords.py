import argon2
from argon2 import PasswordHasher

ph = PasswordHasher()

class PW_HANDLER:
  def __init__(self, password: str):
    self.password = password

  def hashing(self) -> str:
    self.hash = ph.hash(self.password)
    if ph.check_needs_rehash(self.hash):
      self.hash = ph.hash(self.password)
      return self.hash
    return self.hash

  def verify(self, hashed_password, input: str) -> bool:
    try:
      ph.verify(hashed_password, input)
      return True
    except argon2.exceptions.VerifyMismatchError:
      return False