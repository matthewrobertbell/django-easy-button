def randHash40(*args):
  """
    Generates a universally unique ID.
    Any arguments only create more randomness.
  """
  import time, random, hashlib
  t = long( time.time() * 1000 )
  r = long( random.random()*100000000000000000L )
  try:
    a = socket.gethostbyname( socket.gethostname() )
  except:
    # if we can't get a network address, just imagine one
    a = random.random()*100000000000000000L
  data = str(t)+' '+str(r)+' '+str(a)+' '+str(args)
  return hashlib.sha1(data).hexdigest()

def randHash8(*args):
    return randHash40(*args)[:8]
