import typing
from prime import get_random_prime, get_random_coprime

class Key:
  def __init__(self, n:int):
    self.n = n

class PrivateKey(Key):
  __slots__ = ['d', 'n']

  def __init__(self, d:int, n:int): 
    self.d = d
    self.n = n

class PublicKey(Key):
  __slots__ = ['e', 'n']

  def __init__(self, e:int, n:int):
    self.e = e
    self.n = n

def generate_keys(nbytes: int) -> typing.Turple[PrivateKey, PublicKey]:
  """ n, O, e, d 값 결정
  p = prime number
  q = prime number
  n = p * q
  O = Phi_n = (p-1)*(q-1)
  e = O의 서로소
  d, (d*e)%O = 1인 수. (d<O)
   -> d%O = (1/e)%O
   -> d = e^(O-2)%O
   -> d = e^(O-2)%O
  """
  p = get_random_prime(nbytes) # p는 nbytes/2길이의 소수
  q = get_random_prime(nbytes) # q는 nbytes/2길이의 소수
  n = p*q
  O = (p-1)*(q-1)
  e = get_random_coprime(val=O, limit=n) # e는 n보다 작은 O의 서로소
  d = pow(e, O-2, O)
  
  del p, q, O

  return PrivateKey(d, n), PublicKey(e, n) # 개인키, 공개키