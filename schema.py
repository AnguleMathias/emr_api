import graphene
import api.role.schema
import api.user.schema
import api.user.schema_query


class Query(
    api.role.schema.Query,
    api.user.schema_query.Query
):
    """Root for emr Graphql queries"""
    pass


class Mutation(
    role.schema.Mutation,
    api.user.schema.Mutation
):
    """Root for graphql mutations"""
    pass


schema = graphene.Schema(query=Query, mutation=Muta)
