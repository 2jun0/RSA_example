from util import get_random_odd_int
import random

def get_primality_testing_rounds(num: int) -> int:
  """밀러-라빈 소수 판정법을 수행할 때, 반복할 횟수를 구한다.
  
  1300 <= num:  k = 2
  850 <= num:    k = 3
  650 <= num:    k = 4
  300 <= num:    k = 10
  300 > num:    k = 30

  ref : http://cacr.uwaterloo.ca/hac/about/chap4.pdf
  """

  nbits = num.bit_length()
  if nbits >= 1300:
    return 2
  if nbits >= 850:
    return 3
  if nbits >= 650:
    return 4
  if nbits >= 300:
    return 10
  
  return 30

def miller_rabin_primality_testing(n: int, k: int) -> bool:
  if n < 2:
    return False

  # n - 1 => (2 ** r) * d
  # d가 짝수이면 계속 2로 나눔
  d = n - 1
  r = 0

  while not (d & 1):
    r += 1
    d >>= 1

  # k번 테스트
  for _ in range(k):
    a = random.randint(2, n - 3)

    x = pow(a, d, n)
    if x == 1 or x == n - 1:
      continue

    for _ in range(r - 1):
      x = pow(x, 2, n)
      if x == 1:
        # n는 합성수.
        return False
      if x == n - 1:
        # 나머지가 -1인 경우
        # n는 합성수가 아닐 것임.
        # 다음 판정을 시작한다. 
        break
    else:
      # 합성수의 모든 조건을 만족함
      # n는 합성수
      return False

  return True


def is_prime(int_val: int) -> int:
  # Check for small numbers.
  if int_val < 10:
    return int_val in [2, 3, 5, 7]

  # Check for even numbers.
  if not (int_val & 1):
    return False
  
  k = get_primality_testing_rounds(int_val)

  return miller_rabin_primality_testing(int_val, k)

def are_coprime(a: int, b: int) -> bool:
  # 서로소인지 확인한다.
  return gcd(a,b) == 1


def get_random_prime(nbytes: int) -> int:
  assert nbytes > 0 # the loop wil hang on too small numbers

  while True:
    int_val = get_random_odd_int(nbytes)

    # Test if it is a prime number
    if is_prime(int_val):
      return int_val
    
      # If not, retry

def get_random_coprime(val, limit, iter_max = 10000): # 임의의 서로소 구하기
  for _ in range(iter_max = 10000):
    num = random.randint(limit)
    if gcd(val, num) == 1:
      return num
  raise RuntimeError('unable to find coprime')