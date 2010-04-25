known_physics_laws = []

def learn_law(law):
    known_physics_laws.append(law())

try:
  import Time
except:
  print "Couldn't import Time Physics"

try:
  import WifiLocation
except:
  print "Couldn't import WifiLocation Physics"
