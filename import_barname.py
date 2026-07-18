import pandas as pd

from app import app
from models import db, Barname

df = pd.read_excel("static/data/barname.xlsx")

with app.app_context():

    for _, row in df.iterrows():

        item = Barname(

            waybill=row["شماره بارنامه"],

            sender=row["فرستنده"],

            marketer=row["بازاریاب"],

            weight=row["وزن"],

            service=row["نوع سرویس"],

            upload_date=row["تاریخ بارگذاری"]

        )

        db.session.add(item)

    db.session.commit()

print("Done")
