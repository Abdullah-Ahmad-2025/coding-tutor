from database import SessionLocal
from models.schema import Submission

db = SessionLocal()
subs = db.query(Submission).all()
for s in subs:
    print(f"Submission: {s.id}, passed={s.passed}")
db.close()
