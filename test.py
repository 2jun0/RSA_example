from encript import encript, encript_file
from decript import decript, decript_file

# 입력된 값 테스트
val = input('문자열을 입력해주세요 : ')
print('입력된 값 : {}'.format(val.encode('utf-8')))
encripted_val, private_key, public_key = encript(val.encode('utf-8'))
print(f'암호화된 값 : {encripted_val}, 개인키 : {private_key}, 공개키 : {public_key}')
decripted_val = decript(encripted_val, public_key)
original_val = decripted_val.decode('utf-8')
print(f'복호화된 값 : {decripted_val} = {original_val}')

# 파일 암호화 테스트
print('-원본 파일 내용-')
f = open('./테스트.txt', 'rt', encoding='utf-8')
for line in f.readlines():
	print(line, end='')
f.close()
print('')
private_key, public_key = encript_file('./테스트.txt')
print(f'-암호화된 파일 내용, 개인키 : {private_key}, 공개키 : {public_key}-')
f = open('./테스트.txt.dat', 'rb')
for line in f.readlines():
	print(line, end='')
f.close()
print('')
decript_file('./테스트.txt.dat', public_key)
print(f'-복호화된 파일 내용-')
f = open('./테스트.txt', 'rt', encoding='utf-8')
for line in f.readlines():
	print(line, end='')
f.close()