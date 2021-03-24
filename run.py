from suslab import app, get_app()

handler = app.get_app()

if __name__ == '__main__':
    app.run(debug=True)
