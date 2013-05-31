
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

  def value(self):
    ret = 1
    for (k,v) in self.factors.items():
      for i in range(0,v):
        ret *= k
    return ret

  # Chinese remainder theorem...
  def crt(self):
    primes = self.factors.keys()
    n = self.value()
    primes.sort()
    ret = []
    factors = [ (p**self.factors[p]) for p in primes ]

    for a in factors:
      v = 1
      for b in factors:
        if a != b:
          (ainv,_) = egcd(a, b)
          v = (v*a*ainv)%n
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

d = [0]*6
for i in range(0,3):
  d[i] = A(i,i)
print d

#----------------------------------------

# log_2(f(a,infinity)), for small values of a...
small_f =     [ 0, 2, 4, 16, 65536 ]
log_small_f = [ 0, 1, 2, 4, 16, 65536 ]

def f(a,n):
  val = n.value()
  print "+> f({0},{1})".format(a,val)
  if val <= 1: return 0
  if a == 1: return (2%val)

  if n.n_factors() == 1:

    if n.first_factor() == 2:
      e = n.exp(2)
      # 2^2^..2^2 >= 2^e, so just 0
      if a >= len(log_small_f) or e <= log_small_f[a]:
        ret = 0
      else:
        ret = small_f[a]

    else:
      # Finally, a recursive case!
      x = f(a-1,n.phi())
      ret = mod_exp(2,x,val)

  else:
    # compute the chinese remainder factors
    (primes, crf) = n.crt()
    print "CRT {0} -> ".format(val)
    print "  " + str(n)
    print "  " + str(primes)
    print "  " + str(crf)
    tot = 0
    for (i,p) in enumerate(primes):
      x = f(a,n.break_off(p))
      tot = (tot + x*crf[i]) % val
    ret = tot
  print "-> f({0},{1}) -> {2}".format(a,val,ret)
  return ret

#----------------------------------------

N = PrimeFactorization.factorize(14**8)

print f(3,N)


