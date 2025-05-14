
from app import app

# Add support for custom domains in the development environment
if __name__ == "__main__":
    # Enable debug mode in development
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
