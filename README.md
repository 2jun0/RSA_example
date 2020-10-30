# RSA_example
 RSA를 이용한 암호화 알고리즘

# 사용법

## 테스트 해보기
`py test.py`

## 암호화
블럭크기는 기본값이 2(2bytes) 입니다.

문자열 암호화 하기

`py encript.py -s [문자열] -b [선택: 블럭 크기]`

파일 암호화하기

`py encript.py -f [파일 위치] -b [선택: 블럭 크기]`

"파일이름.dat"에 암호화된 파일이 저장됩니다.

## 복호화
문자열 복호화 하기

`py encript.py -s [문자열] -pk [공개키 ex) 1,3] -b [선택: 블럭 크기]`

파일 복호화하기

`py encript.py -f [파일 위치] -pk [공개키 ex) 1,3] -b [선택: 블럭 크기]`
