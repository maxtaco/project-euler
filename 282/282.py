

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

class PrimeFactorization:

  PRIMES = [ 2,3,5,7,11,13,17,19,23 ]

  def __init__ (self, factors):
    self.factors = factors

  def phi(self):
    d = PrimeFactorDict()
    for (k,v) in self.factors.items():
      if v > 1:
        d.inc(k,v-1)
      if k > 2:
        tmp = PrimeFactorization.factorize(k-1)
        d.merge(tmp)
    return PrimeFactorization(d)

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

def mod_exp (b,x,m):
  if m <= 1: return 0
  ret = 1
  while x > 0:
    if (x & 0x1):
      ret = (b*ret)%m
    b = (b*b)%m
    x = x >> 1
  return ret

print PrimeFactorization.factorize(2*3*3*5*5*7*7*11*11*11*11).value()