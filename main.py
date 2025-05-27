from models import Session, WindowType

session = Session()
for wt in session.query(WindowType).all():
    print("-", wt.name)
session.close()
