import amusepark

app = amusepark.create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5555, debug=True)
