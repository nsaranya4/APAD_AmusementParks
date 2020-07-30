from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)   

@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method =='POST':
        try:
            print ("came here 2")
            return redirect(url_for('manage'))
        except: 
            return 'There was an issue logging in'

    return render_template('login.html')

@app.route('/viewing', methods= ['GET','POST'])
def viewing():
    if request.method=='POST':
        try:
            print('came here 3')
            return redirect(url_for('singleTheme'))
        except:
            return 'There was an issue going to single theme page'
    else:
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

@app.route('/singleTheme')
def singleTheme():

    return render_template('singleTheme.html')

@app.route('/newreport', methods=['POST','GET'])
def newReport():
    if request.method == 'POST':
        print('came here 5')
        post.done = request.form['Done']
        post.cancel = request.form['Cancel']
        new_post = Todo(Done=post_Done, Cancel=post_cancel)
        try:
            db.session.add(new_post)
            db.session.commit()
            print ("came here 1")
           #return redirect('/')
            return redirect(url_for('singleTheme'))
        except:
            return 'There was an issue adding a theme'
        finally:
            db.session.add(new_post)
            db.session.commit()
           #return redirect('/')
            return redirect(url_for('singleTheme'))
    else:
        return render_template('newreport.html',  post= posts)



if __name__ == "__main__":
    app.run(debug=True)