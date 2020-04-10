from graphql import GraphQLError

from api.user.models import users_roles


def filter_by_role(query, role):
    query = query.join(users_roles)
    return query.filter_by(role_id=role)
