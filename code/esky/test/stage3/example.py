from __future__ import print_function

import sys
import esky

if getattr(sys,"frozen",False):
    #app = esky.Esky(sys.executable,"https://example-app.com/downloads/")
    app = esky.Esky(sys.executable,"http://localhost:8000")
    try:
        if(app.find_update() != None):
            print("NEW UPDATE AVAILABLE! DO YOU WANT TO UPDATE?")
            confirm = input()
            if(confirm == "y"):
                app.auto_update()
                print("UPDATE IS SUCCESFULL! NEXT TIME YOU'LL SEE THE CHANGES!")
            else:
                print("MAYBE NEXT TIME")
    except Exception as e:
        print ("ERROR UPDATING APP:", e)

print("HELLO AGAAIN WORLD - Stage 3")

