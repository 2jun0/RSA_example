import os
from util import get_bytes_length
from key import PublicKey

def encrypt_int(int_val:int, key:PublicKey) -> int:
	return pow(int_val, key.e, key.n)

def _pad_data(data: bytes, key_len: int) -> bytes:
	max_data_len = key_len - 11
	data_len = len(data)

	if data_len > max_data_len:
		raise OverflowError('%i bytes needed for data, but there is only '
												' space for %i' % (data_len, max_data_len))
	
	# Get random padding
	padding_len = key_len - data_len - 3
	padding = b''

	# Padding에 \x00은 넣지 않는다.
	# \x00이 나올 경우 지운채로 붙인다.
	while len(padding) < padding_len:
		needed_padding_len = padding_len - len(padding)

		new_padding = os.urandom(needed_padding_len)
		new_padding = new_padding.replace(b'\x00', b'')
		padding += new_padding

	assert len(padding) == padding_len

	return b''.join([b'\x00\x02',
									padding,
									b'\x00',
									data])


def encrypt_block(data: bytes, key: PublicKey) -> bytes:
	"""data를 암호화한다.

	- overflow를 방지하기 위해 다음을 만족해야 한다.
		len(data) <= len(key) + 11

	- 11인 이유는 
		(오버플로우 방지 1바이트)8 + (패딩 비트)3
	"""

	key_len = get_bytes_length(key.n)
	padded = _pad_data(data, key_len)

	int_data = int.from_bytes(padded, byteorder='big')
	encrypted = encrypt_int(int_data, key)
	block = encrypted.to_bytes(key_len, byteorder='big')

	return block

def encrypt(data: bytes, key: PublicKey) -> bytes:
	key_len = get_bytes_length(key.n)
	max_data_len = key_len-11

	encrypted = b''
	for i in range(0, len(data), max_data_len):
		encrypted += encrypt_block(data[i:i+max_data_len], key)

	return encrypted

def encrypt_file(src: str, dest: str, key: PublicKey):
	key_len = get_bytes_length(key.n)
	max_data_len = key_len-11

	try:
		rf = open(src, 'rb')
		wf = open(dest, 'wb')
		data = 1
		while data != b"":
			data = rf.read(max_data_len)
			encrypted_data = encrypt_block(data, key)
			wf.write(encrypted_data)
	finally:
		rf.close()
		wf.close()