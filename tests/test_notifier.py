import sys
import os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')
from genshinhelper import notifiers


#notifiers.Bark().send('title', 'status', 'desp')

notifiers.send('title', 'status', 'desp')
