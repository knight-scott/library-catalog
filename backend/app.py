from flask import Flask 
from routes.books import books_bp
# uncomment when libraries blueprint is complete
# from routes.libraries import libraries_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(books_bp, url_prefix='/api/books')
# uncomment when libraries blueprint is complete
# app.register_blueprint(libraries_bp, url_prefix='/api/libraries')
# continue for genres and users

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
