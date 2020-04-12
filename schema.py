import graphene
import api.role.schema
import api.user.schema
import api.user.schema_query
import api.notification.schema


class Query(
    api.role.schema.Query,
    api.user.schema_query.Query,
    api.notification.schema.Query,
):
    """Root for emr Graphql queries"""
    pass


class Mutation(
    api.role.schema.Mutation,
    api.user.schema.Mutation,
    api.notification.schema.Mutation,
):
    """Root for graphql mutations"""
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
