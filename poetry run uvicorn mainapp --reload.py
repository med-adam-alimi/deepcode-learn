"poetry run uvicorn main:app --reload"


def modp(n, p):
    if n == 0:
        return 1 % p
    result = 1
    power = 2 % p
    while n > 0:
        if n % 2 == 1:
            result = (result * power) % p
        power = (power * power) % p
        n = n // 2
    return result 

