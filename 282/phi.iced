

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

# note from the above this doesn't work for arbitrary numbers,
# since we only have so many prime factors :)
n = Factorization.factorize Math.pow(14,8)
console.log "n=14^8"
for i in  [0...25]
  console.log "phi_#{i} -> #{n.toString()}"
  n = n.phi()



