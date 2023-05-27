def metodes():
  mm = "miya"
  mage = "odet"
  
  return (mm, mage)

import os

__dir__ = os.path.dirname(os.path.abspath(__file__))
print (os.path.abspath(__file__))
print (metodes())
print (os.path.dirname(os.path.abspath(__file__)))
print (os.path.abspath(os.path.join(__dir__, '..')))