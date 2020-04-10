from graphql import GraphQLError

from api.user.models import users_roles


def user_filter(query, filter_data):
    role = filter_data.get('role_id', None)

    elif role and not location:
        return filter_by_role(query, role)
    elif all([location, role]):
        query = filter_by_location(query, location)
        return filter_by_role(query, role)
    else:
        return query


def filter_by_role(query, role):
    query = query.join(users_roles)
    return query.filter_by(role_id=role)
