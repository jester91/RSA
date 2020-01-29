import random
import sys

sys.setrecursionlimit( 1000000 )  # long type,32bit OS 4B,64bit OS 8B(1bit for sign)

"""Kibovitett eukledeszi módszer ami vissza adja a (g, x, y) a*x + b*y = gcd(x, y) értéket, rekurzív megoldás"""
def egcd(a, b):

    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd( b % a, a )
        return (g, y - (b // a) * x, x)


"""annak csekkolása, hogy a p és q értéke inverz-e, ha nem akkor hibát dob vissza, mivel igy nem használható az a p és q"""
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('mod inverz nem létezik')
    else:
        return x % m

"""visszadja a multiplikativ inverzét  b modulo n-nek"""
def mulinv(b, n):
    g, x, _ = egcd( b, n )
    if g == 1:
        return x % n


"""miller rabin teszt n a tesztelendő szám k pedig a teszt elvégzésének a száma"""
def miller_rabin(n, k):
    if n == 2:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range( k ):
        a = random.randrange( 2, n - 1 )
        x = power( a, s, n )
        if x == 1 or x == n - 1:
            continue
        for _ in range( r - 1 ):
            x = power( x, 2, n )
            if x == n - 1:
                break
        else:
            return False
    return True

""""mod pow alternatívája"""
def power(a, n, p):
    res = 1
    a = a % p
    while (n > 0):
        if ((n & 1) == 1):
            res = (res * a) % p
        n = n >> 1
        a = (a * a) % p
    return res


""""itt állíthatjuk be, hogy hány bites prímet szeretnénk generálni és, hogy hányszor szeretnénk lefuttatni a miller rabin tesztet"""
def primtest():
    primtest = 0
    while primtest == 0:
        prim = random.getrandbits( 1024 )
        primtest = miller_rabin( prim, 1 )

    return prim


""""kulcscgenerálás"""
def kulcsgen():
    p = primtest()
    q = primtest()
    n = p * q
    fn = (p - 1) * (q - 1)
    e_gcd = 0
    while e_gcd != 1:
        e = random.randint( 1, 101 )
        e_gcd = mulinv( fn, e )

    k = 1
    d_test = False
    while d_test == False:
        if (k * fn + 1) % e == 0:
            d = (k * fn + 1) // e
            d_test = True
        k += 1
    return (p, q, n, fn, e, d)


p, q, n, fn, e, d = kulcsgen()

def titkositas(m, n, e):
    return power( m, e, n )

""""p és q értéke az m1,m2"""
def kinaimaradek(p, q, n, d, c):
    d = int( d )

    x1 = c % p
    x2 = c % q

    fP = d % (p - 1)
    fQ = d % (q - 1)

    x1 = power( x1, fP, p )
    x2 = power( x2, fQ, q )

    M1 = modinv( p, q )
    M2 = modinv( q, p )

    x = (x1 * q * M2 + x2 * p * M1) % n

    return x

print( "p:", p )

print( "q:", q )

print( "n:", n )

print( "f(n):", fn )

print( "e:", e )

print( "d:", d )

m = 1024
print( "m:", m )
c = titkositas( m, n, e )
print( "c kódolt üzenet értéke:" )
print( c )
print( "c kódolt üzenet visszafejtés utáni értéke:" )
print( kinaimaradek( p, q, n, d, c ) )
print( "PK: (e:", e, " n:", n, ")" )
print( "SK: (d:", d, " n:", n, ")" )
