from app import app
from models import User

with app.app_context():
    users = User.query.all()

    print("Count:", len(users))

    for u in users:
        print(u.username, u.marketer)