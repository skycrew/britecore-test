from web.app import app


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True, ssl_context=("config/ssl.crt", "config/ssl.key"))