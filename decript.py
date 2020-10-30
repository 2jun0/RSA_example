from argparse import ArgumentParser
from util import mod_exp

parser = ArgumentParser(description='RSA복호화')
parser.add_argument('-f', '--file_path', action="store", dest="file_path", type=str, help="file path", default=None)
parser.add_argument('-s', '--str', action="store", dest="str", type=str, default=None)
parser.add_argument('-b', '--block_size', action="store", dest="block_size", type=int, default=2)
parser.add_argument('-pk', '--public_key', action="store", dest="public_key", type=str,  required=True)

def decript_block(data:bytes, d, n, block_size=2):
	int_val = int.from_bytes(data, 'big')
	if int_val >= n:
		decripted_int_val = mod_exp(int_val, d, n) + int(int_val / n) * n
	else:
		decripted_int_val = mod_exp(int_val, d, n)
	decripted_data = decripted_int_val.to_bytes(block_size, byteorder='big')

	idx = block_size-1
	while idx >= 0:
		if decripted_data[idx] != 0:
			break
		idx -= 1

	return decripted_data[:idx+1]

def decript(data:bytes, public_key, block_size=2):
	d = public_key[0]
	n = public_key[1]
	if len(data) % block_size != 0:
		data += bytes([0]*(block_size - len(data) % block_size))

	decripted_data = bytes()
	for i in range(0, len(data), block_size):
		decripted_data += decript_block(data[i:i+block_size], d, n)

	return decripted_data

def decript_file(path, public_key, block_size=2):
	try:
		rf = open(path, 'rb')
		wf = open('.'.join(path.split('.')[0:-1]), 'wb')
		data = 1
		while data != b"":
			data = rf.read(block_size)
			decripted_data = decript(data, public_key, block_size)
			wf.write(decripted_data)
	finally:
		rf.close()
		wf.close()

if __name__ == '__main__':
	args = parser.parse_args()
	d, n = map(int, args.public_key.split(','))
	public_key = (d, n)
	if args.str:
		decripted_val = decript_block(args.str, public_key, args.block_size)
		original_val = decripted_val.decode('utf-8')
		print(f'복호화된 값 : {decripted_val} = {original_val}')
	elif args.file_path:
		decript_file(args.file_path, public_key, args.block_size)