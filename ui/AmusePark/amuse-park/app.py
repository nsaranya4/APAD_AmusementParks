from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

@app.route('/')
def viewing():
    themes = [{"name": "Park name", "description": "adfsdfdf"},{"name": "Park name", "description": "adfsdfdf"}, {"name": "Park name", "description": "adfsdfdf"}]
    return render_template('viewing.html', themes=themes)

@app.route('/manage')
def manage():
    subscribes = [{"name": "Park name", "description": "adfsdfdf"},{"name": "Park name", "description": "adfsdfdf"}, {"name": "Park name", "description": "adfsdfdf"}]
    return render_template('manage.html', subscribes=subscribes)
@app.route('/createtheme')
def createTheme():

        return render_template('createtheme.html')



if __name__ == "__main__":
    app.run(debug=True)