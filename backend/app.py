from flask import Flask 
from routes.books import books_bp
from routes.libraries import libraries_bp
from routes.users import users_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(books_bp, url_prefix='/api/books')
app.register_blueprint(libraries_bp, url_prefix='/api/libraries')
app.register_blueprint(users_bp, url_prefix='/api/users')
# continue for genres and users

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
