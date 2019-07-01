from itertools import count, compress, takewhile, cycle
from math import gcd, fsum, log,pow
try:
    from gmpy2 import mpz
except ImportError:
    mpz = int

def prime_sieve(start=1, end=float('inf')): # postponed sieve, by Will Ness
    for c in (2,3,5,7):                     # original code David Eppstein,
        if start <= c <= end:               # start and end added by Oscar Smith
            yield c
        elif end < c:
            return
    sieve = {}                              # Alex Martelli, ActiveState Recipe 2002
    ps = prime_sieve()                      # a separate base Primes Supply:
    p = next(ps) and next(ps)               # (3) a Prime to add to dict
    q = p*p                                 # (9) its sQuare
    for c in count(9,2):                    # the Candidate
        if c in sieve:                      # c’s a multiple of some base prime
            s = sieve.pop(c)                # i.e. a composite ; or
        elif c < q:
            if start <= c <= end:
                yield c                     # a prime
                continue
            elif end < c:
                return
        else:   # (c==q):            # or the next base prime’s square:
            s=count(q+2*p,2*p)       #    (9+6, by 6 : 15,21,27,33,...)
            p=next(ps)               #    (5)
            q=p*p                    #    (25)
        for m in s:                  # the next multiple
            if m not in sieve:       # no duplicates
                break
        sieve[m] = s                 # original test entry: ideone.com/WFv4f

def mod_mersenne(n, prime, mersenne):
    """ Calculates n % 2^prime-1 where mersenne_prime=2**prime-1 """
    while n > mersenne:
        n = (n & mersenne) + (n >> prime)
    return n if n != mersenne else 0

def pow_mod_mersenne(base, exp, prime, mersenne):
    """ Calculates base^exp % 2^prime-1 where mersenne_prime=2**prime-1 """
    number = 1
    while exp:
        if exp & 1:
            number = mod_mersenne(number * base, prime, mersenne)
        exp >>= 1
        base = mod_mersenne(base * base, prime, mersenne)
    return number

def p_minus1(prime, mersenne, B1, B2):
    """ Does 2**prime-1 have a factor 2*k*prime+1?
        such that the largest prime factor of k is less than limit"""
    log_B1 = log(B1)
    M = mpz(1)
    for p in prime_sieve(end=B1):
        M *= p**int(log_B1/log(p))
    M = pow_mod_mersenne(3, 2*M*prime, prime, mersenne)
    g = gcd(mersenne, M-1)
    if 1 < g < mersenne:
        return True
    if g == mersenne:
        return False
    return p_minus1_stage_2(prime, mersenne, M, p, B2)


def p_minus1_stage_2(prime, mersenne, M, B1, B2):
    delta_cache = {0:M}
    delta_max = 0
    S = mod_mersenne(M*M, prime, mersenne)
    p_old = B1
    HQ = M
    for k, p in enumerate(prime_sieve(start=B1, end=B2)):
        delta = p - p_old
        if delta not in delta_cache:
            for d in range(delta_max, delta, 2):
                delta_cache[d+2] = mod_mersenne(delta_cache[d] * S, prime, mersenne)
                delta_max = delta
        HQ = mod_mersenne(HQ*delta_cache[delta], prime, mersenne)
        M = mod_mersenne(M*(HQ-1), prime, mersenne)
        p_old = p
        if k % 100 == 0:
            g = gcd(M, mersenne)
            if 1 < g < mersenne:
                return True
            if g == mersenne:
                return False
    return 1 < gcd(M, mersenne) < mersenne

if __name__ == '__main__':
    primes =[693029274887353228407241634151666394848735790190615012301892319642252043063441848065716981473964772442758740370147046907610931634092918165021079036177362202111606191956418667584361908276118660423367531586528459110446538285556884064171765200923553991719010617219127236546574523638048350982056281625504368802910163823494559412837552527875343392553408538829400672258371166335106950477308076204615614002674078815990333298949792313414447948554863231405126552767821926863542808760806617307175797842493616569408376748813625064500486610855810346855210287339165197986553654602677812521680748485202471044713053183325655849850997212737083080466361085135767845684389568237981315538711572490435547358716105872380307864256754216659697090488815080191668745091862519968395816165962906971976332747183909682018887880730856165892484276277315514729408134825829435787368836101082383777555602109552666946636274769705939102192515512772214165267762974326870938422311435887780687375502822263104262793144084464266516328466921283433546722681655409668160240996661786900031559973837193865566010853663246854051817155542757612318538142879371196485283181654007531624894102938084847401272297968117074664980694267271434859758912794604099694079778856636033918615329139]
    for prime in primes:
        B1 = int(10*prime.bit_length())
        p_minus1(prime, pow(mpz(2),mpz(prime-1)), B1, 10*B1)
        if prime>2000:
             break