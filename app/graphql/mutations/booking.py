import strawberry
from app.graphql.types.booking import BookingType, CreateBookingInput
from app.core.database import SessionLocal
from app.models.booking import Booking
from app.models.property import Property
from datetime import datetime
from typing import Optional

@strawberry.type
class BookingMutation:


     @strawberry.mutation
     def book_viewing(self, input:CreateBookingInput) -> BookingType:
          db = SessionLocal()
          try:
                prop = db.query(Property).filter(Property.id == input.property_id).first()
                if not prop:
                     raise ValueError("Property not found")

                new_booking = Booking(
                     property_id=input.property_id,
                     buyer_id=input.buyer_id,
                     booking_date= datetime.strptime(input.booking_date, "%Y-%m-%d"),
                     status="pending",
                )

                db.add(new_booking)
                db.commit()
                db.refresh(new_booking)

                return  BookingType(
                     id= new_booking.id,
                     property_id=new_booking.property_id,
                    buyer_id=new_booking.buyer_id,
                    booking_date=str(new_booking.booking_date),
                    status=new_booking.status,
                    property_title=new_booking.property.title,
                    buyer_name=new_booking.buyer.name,
                )
          finally:
               db.close()

     @strawberry.mutation
     def update_booking_status(self, id:int, status:str) -> Optional[BookingType]:
          db = SessionLocal()
          try:
               booking = db.query(Booking).filter(Booking.id == id).first()
               if not booking:
                    return None

               booking.status = status
               db.commit()
               db.refresh(booking)

               return BookingType(
                    id = booking.id,
                    property_id=booking.property_id,
                    buyer_id=booking.buyer_id,
                    booking_date=str(booking.booking_date),
                    status=booking.status,
                    property_title=booking.property.title,
                    buyer_name=booking.buyer.name,
               )

          finally:
               db.close()