
#----------------------------------------

class PrimeFactorDict (dict):
  def inc(self,k,i):
    if self.get(k):
      self[k] += i
    else:
      self[k] = i
  def __str__ (self):
    keys = self.keys()
    keys.sort()
    return "{" + ", ".join([ "{0}^{1}".format(k, self[k]) for k in keys ]) + "}"
  def copy (self):
    r = PrimeFactorDict()
    for (k,v) in self.items():
      r[k] = v
    return r
  def merge (self, d):
    for (k,v) in d.items():
      self.inc(k,v)
  def first (self) :
    return self.keys()[0]

#----------------------------------------

class PrimeFactorization:

  PRIMES = [ 2,3,5,7,11,13,17,19,23 ]

  def __init__ (self, factors):
    self.factors = factors

  def __str__(self): return str(self.factors)

  def phi(self):
    d = PrimeFactorDict()
    for (k,v) in self.factors.items():
      if v > 1:
        d.inc(k,v-1)
      if k > 2:
        tmp = PrimeFactorization.factorize(k-1)
        d.merge(tmp.factors)
    return PrimeFactorization(d)

  def n_factors(self):
    return len(self.factors)
  def first_factor(self):
    return self.factors.first()
  def exp(self,a):
    return self.factors[a]

  @classmethod
  def factorize (klass, n):
    d = PrimeFactorDict()
    for f in klass.PRIMES:
      tmp = n
      i = 0
      go = True
      while go:
        (q,r) = divmod(tmp,f)
        if r == 0:
          tmp = q
          i += 1
        else:
          go = False
      if i > 0:
        d.inc(f,i)
    return PrimeFactorization(d)

  def __int__(self):
    ret = 1
    for (k,v) in self.factors.items():
      for i in range(0,v):
        ret *= k
    return ret

  # Chinese remainder theorem...
  def crt(self):
    primes = self.factors.keys()
    n = int(self)
    primes.sort()
    ret = []
    factors = [ (p**self.factors[p]) for p in primes ]

    for a in factors:
      r = n/a
      (rinv,_) = egcd(r, a)
      v = (r*rinv)%n
      ret.append(v)
    return [primes, ret]

  def break_off(self,prime):
    d = PrimeFactorDict()
    d[prime] = self.exp(prime)
    return PrimeFactorization(d)

#----------------------------------------

def mod_exp (b,x,m):
  if m <= 1: return 0
  ret = 1
  while x > 0:
    if (x & 0x1):
      ret = (b*ret)%m
    b = (b*b)%m
    x = x >> 1
  return ret

#----------------------------------------

# http://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
def egcd (a,b):
  lastx = 1
  lasty = 0
  x = 0
  y = 1
  while b != 0:
    (quotient,rem) = divmod(a,b)
    (a,b) = (b, rem)
    (x, lastx) = (lastx - quotient * x, x)
    (y, lasty) = (lasty - quotient * y, y)
  return (lastx, lasty)

#----------------------------------------

def phi(n): 
  f = PrimeFactorization.factorize(n)
  return f.phi().value()

#----------------------------------------

def A(m,n):
  if m is 0: return n+1
  elif n is 0: return A(m-1,1)
  else: return A(m-1,A(m,n-1))

#----------------------------------------

d = [0]*7
for i in range(0,4):
  d[i] = A(i,i)

#----------------------------------------

# log_2(f(a,infinity)), for small values of a...
small_f =     [ 0, 2, 4, 16, 65536 ]
log_small_f = [ 0, 1, 2, 4, 16, 65536 ]

# compute 2^2^...^2 a times, modulo m
def f(a,m_pf):

  # m_pf is a prime factorization of m.  m now is the integer value of it
  m = int(m_pf)

  # base cases
  if m <= 1: return 0
  if a == 1: return (2%m)

  if m_pf.n_factors() == 1:

    # If m is a power of 2, it's a special case we need to deal with,
    # since we have a base of 2 for our exponentiation as well.
    if m_pf.first_factor() == 2:
      # The exponent that is applied to 2 in this factorization
      e = m_pf.exp(2)

      # 2^2^..2^2 >= 2^e, so just 0
      if a >= len(log_small_f) or e <= log_small_f[a]:
        ret = 0
      else:
        # Otherwise, no need to mod, since it's less than the modulus
        ret = small_f[a]

    else:
      # Finally, a recursive case! If gcd(2,n) = 1, then we
      # can simplify the exponentiation and take the exponent
      # modulo phi(n).  So here goes, first compute the exponent:
      x = f(a-1,m_pf.phi())

      # now actually do the exponentiation, but we know that x < m,
      # which is helpful
      ret = mod_exp(2,x,m)

  else:
    # compute the chinese remainder factors.
    (primes, crf) = m_pf.crt()

    ret = 0
    for (i,p) in enumerate(primes):

      # Compute f recursively on all of the prime factors
      x = f(a,m_pf.break_off(p))

      # And chinese remainder them back together....
      ret = (ret + x*crf[i]) % m
      
  return ret

#----------------------------------------

N = PrimeFactorization.factorize(14**8)
d[4] = f(7,N)-3 # as per ackermann definition
d[5] = f(100,N)-3 # since everything over 10 or so is the same...
d[6] = d[5] # see above...

print d

ret = 0
for i in d:
  ret = (ret + i) % int(N)
print ret

