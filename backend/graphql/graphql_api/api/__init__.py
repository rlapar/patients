import graphene

from .query import Query

schema = graphene.Schema(query=Query, auto_camelcase=False)
