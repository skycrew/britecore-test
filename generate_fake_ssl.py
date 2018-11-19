# Generate fake ssl cert for development purposes
from werkzeug.serving import make_ssl_devcert

make_ssl_devcert("./config/ssl", host="localhost")
