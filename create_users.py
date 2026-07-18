import pandas as pd
from werkzeug.security import generate_password_hash

from app import app
from models import db, User

df = pd.read_excel("users.xlsx")

with app.app_context():

    for _, row in df.iterrows():

        username = str(row["username"]).strip()

        if User.query.filter_by(username=username).first():
            continue

        user = User(
            username=username,
            marketer=str(row["full_name"]).strip(),
            password=generate_password_hash(str(row["password"])),
            role=row["role"]
        )

        db.session.add(user)

    db.session.commit()

print("Users imported successfully.")