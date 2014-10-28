import os

def path():
    print("os.path.basename(__file__): %s" % os.path.basename(__file__)) # path.py
    print("os.path.dirname(__file__): %s" % os.path.dirname(__file__)) # app/scripts
    print("os.path.abspath(__file__): %s" % os.path.abspath(__file__)) # /Users/gduverger/Sites/hackweek/pixel-perfect/app/scripts/path.py

    print("os.path.dirname(os.path.dirname(__file__)): %s" % os.path.dirname(os.path.dirname(__file__))) # app
    print("os.path.dirname(os.path.abspath(__file__)): %s" % os.path.dirname(os.path.abspath(__file__))) # /Users/gduverger/Sites/hackweek/pixel-perfect/app/scripts

if __name__ == "__main__":
    path()
