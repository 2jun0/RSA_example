from util import get_bytes_length
from key import PrivateKey

def decrypt_int(int_val:int, key:PrivateKey) -> int:
	return pow(int_val, key.d, key.n)

def decrypt_block(block: bytes, key: PrivateKey) -> bytes:
	"""data를 복호화한다.

	:overflow를 방지하기 위해 다음을 만족해야 한다.
	:len(data) <= len(key) + 11
	"""

	block_len = get_bytes_length(key.n)
	encrypted = int.from_bytes(block, byteorder='big')
	decrypted = decrypt_int(encrypted, key)
	clear = decrypted.to_bytes(block_len, byteorder='big')

	if len(block) > block_len:
		raise Exception('Decryption failed')

	# 시작 기호를 찾을 수 없으면 오류
	if clear[0:2] != b'\x00\x02':
		raise Exception('Decryption failed')

	# 두번째 기호를 찾을 수 없으면 오류
	try:
		origin_idx = clear.index(b'\x00', 2)
	except ValueError:
		raise Exception('Decryption failed')
	
	return clear[origin_idx + 1:]

def decrypt(data: bytes, key: PrivateKey) -> bytes:
	block_len = get_bytes_length(key.n)

	decrypted = b''
	for i in range(0, len(data), block_len):
		decrypted += decrypt_block(data[i:i+block_len], key)

	return decrypted

def decrypt_file(src: str, dest: str, key: PrivateKey):
	block_len = get_bytes_length(key.n)

	try:
		rf = open(src, 'rb')
		wf = open(dest, 'wb')
		data = 1
		while data != b"":
			data = rf.read(block_len)
			decrypted = decrypt_block(data, key)
			wf.write(decrypted)
	finally:
		rf.close()
		wf.close()