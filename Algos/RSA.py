from math import sqrt, gcd
from itertools import count, islice
class RSA:
 @staticmethod
 def is_prime(n):
    return n > 1 and all(n % i for i in islice(count(2), int(sqrt(n) - 1)))
 @staticmethod
 def is_relatively_prime(a, b):
    return gcd(a, b) == 1
 def chinese_remainder(self, c, p, q, d):
    dp = d % (p - 1)
    dq = d % (q - 1)
    qinv = self.q_inv(q, p)
    m1 = self.pow_es(c, dp) % p
    m2 = self.pow_es(c, dq) % q
    h = qinv * (m1 - m2) % p
    return m2 + h * q
 @staticmethod
 def q_inv(q, p):
    x = 0
    # Do while xq%p is not equal to 1:
    while x * q % p != 1:
        # Increment x by one:
        x += 1
    return x
 def pow_es(self, base, power):
    # Raise to power by using exponentiation by squaring
    # If power is equal to 1...
    if power == 1:
        # return base value (stop recursion cycle)
        return base
    # If power is even...
    if power % 2 == 0:
        # call same function with squared base half power
        return self.pow_es(base * base, power / 2)
    # If power is odd...
    else:
        # multiply base by value of same function with
        # squared base and half of (power - 1) as arguments
        return base * self.pow_es(base * base, (power - 1) / 2)
 def do_rsa(self, message, p, q, e, action):
    if self.is_prime(p) and self.is_prime(q):
        if self.is_relatively_prime(e, (p - 1) * (q - 1)):
            if action == 'encrypt':
                return {'cipher': self.chinese_remainder(message, p, q, e)}
            elif action == 'decrypt':
                d = self.q_inv(e, (p - 1) * (q - 1))
                return {'message': self.chinese_remainder(message, p, q, d),'D': d}
            elif action == 'both':
                d = self.q_inv(e, (p - 1) * (q - 1))
                cipher = self.chinese_remainder(message, p, q, e)
                return {'cipher': cipher,'message': self.chinese_remainder(cipher, p, q, d),'d': d}
            else:
                raise ValueError('Non available action selected')
        else:
            raise ValueError('{0} is not relatively prime to {1} {2}'.format(e, p, q))
    else:
        raise ValueError('{0} and {1} have to be prime numbers!'.format(p, q))
def test_rsa():
    text = 1314 # 12 # 12007 # 1314 # 120407 # 1314
    e = 343 # 5 # 343 # 12007 # 343
    p = 397 # 5 # 397
    q = 401 # 7 # 401
    rsa = RSA()
    print(rsa.do_rsa(text, p, q, e, 'both'))
if __name__ ==  '__main__':
    test_rsa()
