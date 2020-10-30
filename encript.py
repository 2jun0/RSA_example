from argparse import ArgumentParser
from util import get_random_prime, get_random_coprime, mod_exp

parser = ArgumentParser(description='RSA암호화')
parser.add_argument('-f', '--file_path', action="store", dest="file_path", type=str, help="file path", default=None)
parser.add_argument('-s', '--str', action="store", dest="str", type=str, default=None)
parser.add_argument('-b', '--block_size', action="store", dest="block_size", type=int, default=2)

def encript_block(data:bytes, e, n, block_size=2):
	int_val = int.from_bytes(data, 'big') # 바이트 형식인 data를 int형으로 변환
	if int_val >= n: # 값이 n 보다 큰 경우엔 아래와 같이 수행
		encripted_int_val = mod_exp(int_val, e, n) + (int(int_val / n) * n)
	else:
		encripted_int_val = mod_exp(int_val, e, n) # int_val^e % n
	return encripted_int_val.to_bytes(block_size, byteorder='big')
	
def generate_keys(block_size):
	# n, O, e, d 값 결정
	limit = 256**(block_size/3)
	p = get_random_prime(limit) # p는 block^1/2를 넘지 않는 소수
	q = get_random_prime(limit) # q는 block^1/2를 넘지 않는 소수
	n = p*q 
	O = (p-1)*(q-1)
	e = get_random_coprime(val=O, limit=n) # e는 n보다 작은 O의 서로소
	# d는 (e*d) % O == 1인 수
	d = 0
	for d_tmp in range(1, O):
		if (e*d_tmp) % O == 1:
			d = d_tmp
			break

	return (e, n), (d, n) # 개인키, 공개키

def encript(data:bytes, block_size=2):
	pri_key, pub_key = generate_keys(block_size)
	e = pri_key[0]
	d = pub_key[0]
	n = pri_key[1]

	# data의 길이가 블록사이즈에 맞지 않으면 더미데이터(\x00)을 붙힘
	if len(data) % block_size != 0:
		data += bytes([0]*(block_size - len(data) % block_size))

	encripted_data = bytes() # 암호화된 데이터
	for i in range(0, len(data), block_size): # 블럭단위로 반복
		encripted_data += encript_block(data[i:i+block_size], e, n, block_size)

	return encripted_data, (e, n), (d, n)

def encript_file(path, block_size=2):
	pri_key, pub_key = generate_keys(block_size)

	try:
		rf = open(path, 'rb')
		wf = open(path+'.dat', 'wb')
		data = 1
		while data != b"":
			data = rf.read(block_size)
			encripted_data = encript_block(data, pri_key[0], pri_key[1], block_size)
			wf.write(encripted_data)
	finally:
		rf.close()
		wf.close()

	return pri_key, pub_key

if __name__ == '__main__':
	args = parser.parse_args()
	if args.str:
		encripted_val, private_key, public_key = encript(args.str.encode('utf-8'), args.block_size)
		print(f'암호화된 값 : {encripted_val}, 개인키 : {private_key}, 공개키 : {public_key}')
	elif args.file_path:
		private_key, public_key = encript_file(args.file_path, args.block_size)
		print(f'개인키 : {private_key}, 공개키 : {public_key}')