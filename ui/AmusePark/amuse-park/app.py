from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)



@app.route('/')
def login():
    return render_template('login.html')

@app.route('/viewing')
def viewing():
    themes = [{"name": "Park name", "description": "adfsdfdf"},{"name": "Park name", "description": "adfsdfdf"}, {"name": "Park name", "description": "adfsdfdf"}]
    return render_template('viewing.html', themes=themes)

@app.route('/manage')
def manage():
    posts = [{"title": "Post Title", "name": "Author name", "description": "adfsdfdf"}, {"title": "Post Title", "name": "Author name", "description": "adfsdfdf"},]
    subscribes = [{"name": "Park name", "description": "adfsdfdf"},{"name": "Park name", "description": "adfsdfdf"}, {"name": "Park name", "description": "adfsdfdf"}]
    return render_template('manage.html', subscribes=subscribes, posts=posts)
@app.route('/createtheme')
def createTheme():

    return render_template('createtheme.html')

@app.route('/singletheme')
def singleTheme():

    return render_template('singletheme.html')

@app.route('/newreport')
def newReport():

    return render_template('newreport.html')



if __name__ == "__main__":
    app.run(debug=True)