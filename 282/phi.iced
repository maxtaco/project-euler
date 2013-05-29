

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
  a = 1
  for i in [0...x]
    a = (a*b)%m
  a

n = Factorization.factorize Math.pow(14,8)
f = (a,n) ->
  if n is 1 then return 0
  if a is 0 then return 1
  if a is 1 
    console.log "last phi is #{n}"
    return 2
  x = f(a-1, n.phi())
  ret = mod_exp 2, x, n.value()
  return ret

console.log "n is #{n.value()}"
for i in [20...28]
  v = f i, n
  console.log "#{i} -> #{v}"


