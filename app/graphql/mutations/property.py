import strawberry
from app.graphql.types.property import PropertyType, CreatePropertyInput, UpdatePropertyInput
from app.core.database import  SessionLocal
from app.models.property import Property
from typing import Optional

@strawberry.type
class PropertyMutation:

    @strawberry.mutation
    def create_property(self, input: CreatePropertyInput, agent_id: int) -> PropertyType:
        db = SessionLocal()
        try:
            new_property = Property(
                title=input.title,
                price=input.price,
                city=input.city,
                property_type=input.property_type,
                description=input.description,
                bedrooms=input.bedrooms,
                bathrooms=input.bathrooms,
                area=input.area,
                address=input.address,
                agent_id=agent_id,
                status="available",
            )

            db.add(new_property)
            db.commit()
            db.refresh(new_property)

            return PropertyType(
                id=new_property.id,
                title=new_property.title,
                price=new_property.price,
                city=new_property.city,
                status=new_property.status,
                agent_id=new_property.agent_id,
                description=new_property.description,
                bedrooms=new_property.bedrooms,
                bathrooms=new_property.bathrooms,
                area=new_property.area,
                address=new_property.address,
            )
        finally:
            db.close()

    @strawberry.mutation
    def update_property(self, id: int, input: UpdatePropertyInput) -> Optional[PropertyType]:
        db = SessionLocal()
        try:  
            prop = db.query(Property).filter(Property.id == id).first()
            if not prop:
                return None

            if input.title is not None: prop.title = input.title
            if input.price is not None: prop.price = input.price
            if input.city is not None: prop.city = input.city
            if input.status is not None: prop.status = input.status
            if input.description is not None: prop.description = input.description
            if input.bedrooms is not None: prop.bedrooms = input.bedrooms
            if input.bathrooms is not None: prop.bathrooms = input.bathrooms
            if input.area is not None: prop.area = input.area
            if input.address is not None: prop.address = input.address
            if input.property_type is not None: prop.property_type = input.property_type

            db.commit()
            db.refresh(prop)

            return PropertyType(
                id=prop.id,
                title=prop.title,
                price=prop.price,
                city=prop.city,
                status=prop.status,
                agent_id=prop.agent_id,
                description=prop.description,
                bedrooms=prop.bedrooms,
                bathrooms=prop.bathrooms,
                area=prop.area,
                address=prop.address,
        )
        finally:
            db.close()

    @strawberry.mutation
    def delete_property(self, id: int) -> bool:
        db = SessionLocal()
        try:
            prop = db.query(Property).filter(Property.id == id).first()
            if not prop:
                return False
            db.delete(prop)
            db.commit()
            return True
        finally:
            db.close()
        


    

    