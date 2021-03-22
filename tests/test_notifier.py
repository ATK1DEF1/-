
from genshinhelper import notifiers
import sys
import os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')


notifiers.Bark().send('title', 'status', 'desp')
