import uuid
from database import SessionLocal
from models.schema import User

db = SessionLocal()
user = User(id=str(uuid.uuid4()), email="test@example.com", name="Test User")
db.add(user)
db.commit()
print(f"Created user with ID: {user.id}")
db.close()