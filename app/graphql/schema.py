import strawberry
from app.graphql.queries.property import PropertyQuery
from app.graphql.queries.booking import BookingQuery
from app.graphql.mutations.property import PropertyMutation
from app.graphql.mutations.booking import BookingMutation
from app.core.security import decoded_token
from app.models.user import User
from fastapi import Request
from app.core.database import SessionLocal
from strawberry.fastapi import GraphQLRouter


async def get_context(request: Request) -> dict:
        db = SessionLocal()
        user = None

        token = request.cookies.get("access_token")
        if token:
                try:
                        payload = decoded_token(token)
                        if payload.get("type") == "access":
                                user_id = payload.get("sub")
                                if user_id:
                                        user = db.query(User).filter(User.id == int(user_id)).first()

                except Exception:
                        pass


        return {"db": db, "user": user, "request": request}
@strawberry.type
class Mutation(PropertyMutation, BookingMutation):
               pass
@strawberry.type
class Query(PropertyQuery, BookingQuery):
        pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_router = GraphQLRouter(schema, context_getter=get_context) 