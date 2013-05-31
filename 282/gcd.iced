
egcd = (a,b) ->
  if b is 0 then [1,0]
  else
    q = Math.floor a/b
    r = a % b
    [s,t] = egcd b, r
    [t, s - q*t]

console.log egcd Math.pow(2,8), Math.pow(7,8)