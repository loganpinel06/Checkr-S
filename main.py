#main.py will run the Flask application
#this script imports the createApp function from the app package to create the Flask app instance
#and runs the app through a main guard

#import the createApp method from the app package
from app import createApp

#create the app calling imported subroutine
app = createApp()

#run the app using a main guard
if __name__ == "__main__":
    app.run(debug=True)