import strawberry
from app.graphql.queries.property import PropertyQuery
from app.graphql.mutations.property import PropertyMutation

schema = strawberry.Schema(query=PropertyQuery, mutation=PropertyMutation)