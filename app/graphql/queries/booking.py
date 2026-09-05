import strawberry
from typing import List, Optional
from app.graphql.types.booking import BookingType
from app.core.database import SessionLocal
from app.models.booking import Booking

@strawberry.type
class BookingQuery:

    @strawberry.field
    def my_bookings(self, buyer_id: int) -> List[BookingType]:
        db = SessionLocal()
        try:
            bookings = db.query(Booking).filter(Booking.buyer_id == buyer_id).all()
            return [
                BookingType(
                    id=b.id,
                    property_id=b.property_id,
                    buyer_id=b.buyer_id,
                    booking_date=str(b.booking_date),
                    status=b.status,
                    property_title=b.property.title,
                    buyer_name=b.buyer.name,
                )
                for b in bookings
            ]
        finally:
            db.close()

    @strawberry.field
    def property_bookings(self, property_id: int) -> List[BookingType]:
        db = SessionLocal()
        try:
            bookings = db.query(Booking).filter(Booking.property_id == property_id).all()
            return [
                BookingType(
                    id=b.id,
                    property_id=b.property_id,
                    buyer_id=b.buyer_id,
                    booking_date=str(b.booking_date),
                    status=b.status,
                    property_title=b.property.title,
                    buyer_name=b.buyer.name,
                )
                for b in bookings
            ]
        finally:
            db.close()