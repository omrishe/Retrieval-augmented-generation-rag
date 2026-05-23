#___init.py purpose is to treat this as package (altough not strictly needed, it helps to specify it)
#also as you can see below it can directly expose the variables without needing to specify the file 
#for instace with this i can do from config import STRICT_CLEANING
#while without it will be from config.config import STRICT_CLEANING
from .config import *
