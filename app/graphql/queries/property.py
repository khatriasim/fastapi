import strawberry
from typing import List, Optional
from app.graphql.types.property import PropertyType
from app.core.database import SessionLocal
from app.models.property import Property
from app.models.user import User

@strawberry.type
class PropertyQuery:

    @strawberry.field
    def properties(self, 
                   city:  Optional[str] = None,
                   min_price: Optional[float] = None,
                   max_price: Optional[float] = None,
                   bedrooms: Optional[int] = None,
                   property_type: Optional[str] = None,
                   agent_name: Optional[str] = None, 
                   ) -> List[PropertyType]:
        db = SessionLocal()
        try:
            query = db.query(Property)

            if city:
                query = query.filter(Property.city == city)
            if min_price:
                query = query.filter(Property.price >= min_price)
            if max_price:
                query = query.filter(Property.price <= max_price)
            if bedrooms:
                query = query.filter(Property.bedrooms == bedrooms)
            if property_type:
                query = query.filter(Property.property_type == property_type)
            if agent_name:
                query = query.join(Property.agent).filter(         
                User.name.ilike(f"%{agent_name}%")             
            )                          

            props = db.query.all()
            return [
                PropertyType(
                    id=p.id,
                    title=p.title,
                    price=p.price,
                    city=p.city,
                    status=p.status,
                    agent_id=p.agent_id,
                    agent_name = p.agent.name if p.agent else None,
                    description=p.description,
                    bedrooms=p.bedrooms,
                    bathrooms=p.bathrooms,
                    area=p.area,
                    address=p.address,
                )
                for p in props
            ]
        finally:
            db.close()