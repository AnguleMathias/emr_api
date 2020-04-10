import graphene
from graphene_sqlalchemy import (SQLAlchemyObjectType)
from sqlalchemy import exc
from graphql import GraphQLError

from api.user.models import User as UserModel
from helpers.auth.user_details import get_user_from_db
from helpers.auth.authentication import Auth
from utilities.validator import verify_email
from helpers.auth.error_handler import SaveContextManager
from utilities.utility import update_entity_fields
from api.role.schema import Role
from api.role.models import Role as RoleModel
from helpers.user_role.restrict_admin import check_admin_restriction


class User(SQLAlchemyObjectType):
    """
        Autogenerated return type of a user
    """
    class Meta:
        model = UserModel


class CreateUser(graphene.Mutation):
    """
        Mutation to create a user
    """
    class Arguments:
        email = graphene.String(required=True)
        name = graphene.String(required=True)
        picture = graphene.String()

    user = graphene.Field(User)

    def mutate(self, info, **kwargs):
        user = UserModel(**kwargs)
        if not verify_email(user.email):
            raise GraphQLError("Enter a valid email")
        payload = {
            'model': UserModel, 'field': 'email', 'value':  kwargs['email']
        }
        with SaveContextManager(user, 'User email', payload):
            notification_settings = NotificationModel(user_id=user.id)
            notification_settings.save()
            return CreateUser(user=user)


class DeleteUser(graphene.Mutation):
    """
        Returns payload on deleting a user
    """

    class Arguments:
        email = graphene.String(required=True)
        state = graphene.String()
        remove = graphene.Boolean(default_value=False)

    user = graphene.Field(User)

    @Auth.user_roles('Admin', 'Doctor', 'Default User')
    def mutate(self, info, email, **kwargs):
        if not verify_email(email):
            raise GraphQLError("Invalid email format")
        user_to_be_deleted = User.get_query(
            info).filter_by(email=email).first()
        if not user_to_be_deleted:
            raise GraphQLError("User not found")
        current_user = get_user_from_db()
        if current_user.email == user_to_be_deleted.email:
            raise GraphQLError("You cannot delete yourself")
        should_remove_user = kwargs.get('remove')
        if should_remove_user:
            user_to_be_deleted.delete()
        else:
            update_entity_fields(user_to_be_deleted,
                                 state="archived", **kwargs)
            user_to_be_deleted.save()
        return DeleteUser(user=user_to_be_deleted)


class ChangeUserRole(graphene.Mutation):
    """
        Returns payload on creating a user role
    """
    class Arguments:

        email = graphene.String(required=True)
        role_id = graphene.Int()

    user = graphene.Field(User)

    @Auth.user_roles('Admin', 'Doctor', 'Default User')
    def mutate(self, info, email, **kwargs):
        query_user = User.get_query(info)
        active_user = query_user.filter(UserModel.state == "active")
        exact_user = active_user.filter(UserModel.email == email).first()
        if not exact_user:
            raise GraphQLError("User not found")

        new_role = RoleModel.query.filter_by(id=kwargs['role_id']).first()
        if not new_role:
            raise GraphQLError('invalid role id')

        current_user_role = exact_user.roles[0].role
        if new_role.role == current_user_role:
            raise GraphQLError('This role is already assigned to this user')

        check_admin_restriction(new_role.role)
        exact_user.roles[0] = new_role
        exact_user.save()

        if not notification.send_changed_role_email(
                email, exact_user.name, new_role.role):
            raise GraphQLError("Role changed but email not sent")
        return ChangeUserRole(user=exact_user)


class CreateUserRole(graphene.Mutation):
    """
        Returns payload of creating a role for a user
    """

    class Arguments:
        user_id = graphene.Int(required=True)
        role_id = graphene.Int(required=True)
    user_role = graphene.Field(User)

    def mutate(self, info, **kwargs):
        try:
            user = User.get_query(info)
            exact_user = user.filter_by(id=kwargs['user_id']).first()

            if not exact_user:
                raise GraphQLError('User not found')

            role = Role.get_query(info)
            exact_role = role.filter_by(id=kwargs['role_id']).first()

            if not exact_role:
                raise GraphQLError('Role id does not exist')

            if len(exact_user.roles) > 0:
                raise GraphQLError('This user is already assigned a role')

            exact_user.roles.append(exact_role)
            exact_user.save()

            return CreateUserRole(user_role=exact_user)
        except exc.ProgrammingError:
            raise GraphQLError("The database cannot be reached")


class Mutation(graphene.ObjectType):
    """
        Mutation to create, delete, change_role,
         invite_to_converge and create_user_role
    """
    create_user = CreateUser.Field(
        description="Creates a new user with the arguments\
            \n- email: The email field of the user[required]\
            \n- name: The name field of a user[required]\
            \n- picture: The picture field of a user")
    delete_user = DeleteUser.Field(
        description="Deletes a user having arguments\
            \n- email: The email field of a user[required]\
            \n- state: Check if the user is active, archived or deleted\
            \n- remove: True if it should be a hard delete")
    change_user_role = ChangeUserRole.Field(
        description="Changes the role of a user and takes arguments\
            \n- email: The email field of a user[required]\
            \n- role_id: unique identifier of a user role")
    create_user_role = CreateUserRole.Field(
        description="Assigns a user a role \
            \n- user_id: The  unique identifier of the user\
            \n- role_id:  unique identifier of a user role")
