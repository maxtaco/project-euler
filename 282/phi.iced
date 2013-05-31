

class SmartDict
  constructor : (@d = {}) ->
  inc : (k,i) ->
    if @d[k]? then @d[k] += i
    else @d[k] = i 
  copy : () ->
    r = {}
    r[k] = v for k,v of @d
    return SmartDict r
  dict : -> @d
  toString : () ->
    keys = (Object.keys @d).sort (a,b) -> a-b
    "{" + (("#{k}^#{@d[k]}" for k in keys).join ", ") + "}"
  merge : (d) ->
    for k,v of d.dict()
      @inc k, v

PRIMES = [ 2, 3, 5, 7, 11, 13, 17, 19, 23 ]
class Factorization
  constructor : (@factors) ->
  phi : () ->
    r = new SmartDict()
    for k, v of @factors.dict()
      if v > 1
        r.inc k,(v-1)
      if k > 2
        tmp = Factorization.factorize (k-1)
        r.merge tmp.factors
    return new Factorization r
  toString : () -> @factors.toString()
  @factorize : (n) ->
    d = new SmartDict()
    for f in PRIMES
      tmp = n
      i = 0
      while (tmp % f) is 0
        i++
        tmp = tmp / f
      if i > 0 then d.inc f, i
    return new Factorization d
  value : () ->
    ret = 1
    for k,v of @factors.dict()
      for i in [0...v]
        ret *= k
    ret

# note from the above this doesn't work for arbitrary numbers,
# since we only have so many prime factors :)

mod_exp = (b,x,m) ->
  return 0 if m <= 1
  ret = 1
  while x > 0
    if (x & 0x1) then ret = (b*ret) % m
    b = (b*b) % m
    x = Math.floor(x/2)
  ret

phi = (n) ->
  (Factorization.factorize n).phi().value()

N = Math.pow(14,8)

f = (a,n) ->
  if n <= 1 then return 0
  if a is 1 then return (2%n)
  x = f(a-1, phi(n))
  ret = mod_exp 2, x, n
  return ret

A = (m,n) ->
  if m is 0 then n+1
  else if n is 0 then A(m-1,1)
  else A(m-1,A(m,n-1))

#for i in [0...1000]
#  console.log "#{i} #{f(i,N)}" 
#process.exit 0


d = []
for i in [0..3]
  d[i] = A(i,i)

d[4] = f(4+3, N) - 3
d[5] = f(30,N) - 3
d[6] = d[5]

ret = 0
mod = N
for v in d
  ret = (ret + v) % mod
console.log d
console.log ret
#console.log f(4+3,N)
#console.log f(10000,N)
