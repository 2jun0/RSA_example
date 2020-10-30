import random

prime_list = []
prime_limit = 500

def _init_(): # generate prime numbers
	global prime_list
	
	isPrime = [True] * prime_limit

	for num in range(2,prime_limit):
		if isPrime[num]:
			prime_list.append(num)
			for t_num in range(num, prime_limit, num):
				isPrime[t_num] = False

def get_gcm(a, b): # 최대공약수 구하기
	# 유클리드 호제법을 사용함.
	num = max(a,b)
	div = min(a,b)

	while (num % div) != 0:
		remain = num % div
		num = div
		div = remain
	return div

def mod_exp(num, exp, div):
	x = 1
	pow = num % div

	while exp > 0:
		if exp % 2 == 1:
			x = (x*pow) % div
		pow = (pow*pow) % div	
		exp >>= 1

	return x
		

def get_random_prime(limit):
	global prime_list
	limit_idx = 0
	while limit_idx < len(prime_list):
		if prime_list[limit_idx] >= limit:
			break
		limit_idx+=1

	return prime_list[random.randrange(limit_idx)]

def get_random_coprime(val, limit): # 임의의 서로소 구하기
	coprime_list = []

	for num in range(2, limit):
		if get_gcm(val, num) == 1:
			coprime_list.append(num)

	return random.choice(coprime_list)

_init_()