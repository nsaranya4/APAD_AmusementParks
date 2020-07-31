import amusepark
import os

# calling the function in __init__.py inside pet folder
app = amusepark.create_app()

if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification.

    #start to run the app
    app.run(host='127.0.0.1', port=5555, debug=True)