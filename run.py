# run.py is your application's entry point - it's like the "main" file that starts everything.
#  __init__.py is where you configure your Flask application and its components.


from app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)