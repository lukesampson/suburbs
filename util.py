import os

def relpath(*path):
	basedir = os.path.dirname(os.path.abspath(__file__))
	return os.path.join(basedir, *path)

def readtext(*path):
	f = open(relpath(*path))
	return f.read()