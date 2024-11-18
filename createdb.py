from app import create_app, db
#script to create the Database

app=create_app()

with app.app_context():
    db.create_all()