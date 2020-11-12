from App import create_app

PORT = 5050
HOST = "0.0.0.0"
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=PORT, host=HOST)
