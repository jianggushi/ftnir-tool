from core.model.engine import db
from core.model.light_stability import LightStability


with db.session() as session:
    result = session.query(LightStability).all()
    print(result)
