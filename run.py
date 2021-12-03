from suslab import app, get_app

handler = get_app()

if __name__ == '__main__':
    app.run(debug=True)

