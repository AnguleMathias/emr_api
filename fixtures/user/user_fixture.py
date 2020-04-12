null = None

user_mutation_query = '''
mutation {
  createUser(email: "emr@emr.com"
            name: "this user"
            picture: "www.emr.com/user"){
    user {
      email,
      name,
      picture
    }
  }
}
'''

user_mutation_response = {
    "data": {
        "createUser": {
            "user": {
                "email": "emr@emr.com",
                "name": "this user",
                "picture": "www.emr.com/user"
            }
        }
    }
}

user_duplication_mutation_response = {
    "errors": [{
        "message": "emr@emr.com User email already exists",
        "path": ["createUser"]
    }],
    "data": {
        "createUser": null
    }
}

user_query = '''
query {
    users{
      users{
         email,
      }
   }
}
'''

user_query_response = {
    "data": {
        "users": {
            "users": [
                {
                    "email": "emr@emr.com",
                },
                {
                    "email": "test2@emr.com",
                },
                {
                    "email": "test1@emr.com",
                },
            ]
        }
    }
}

paginated_users_query = '''
query {
    users(page:1, perPage:1){
      users{
         email
      }
      hasNext
      hasPrevious
      pages
   }
}
'''

paginated_users_response = {
    "data": {
        "users": {
            "users": [{
                "email": "test1@emr.com"
            }],
            "hasNext": True,
            "hasPrevious": False,
            "pages": 3
        }
    }
}

query_user_by_email = '''
 query {
  user(email: "test1@emr.com"){
    email
  }
}
'''

query_user_email_response = {
    "data": {
        "user": {
            "email": "test1@emr.com",
        }
    }
}

change_user_role_mutation = '''
mutation{
    changeUserRole(email:"test1@emr.com", roleId: 1){
        user{
            name
            roles{
                role
            }
        }
    }
}
'''

change_user_role_to_super_admin_mutation = '''
mutation{
    changeUserRole(email:"test1@emr.com", roleId: 3){
        user{
            name
            roles{
                role
            }
        }
    }
}
'''

change_user_role_mutation_response = "Role changed but email not sent"

change_user_role_with_already_assigned_role_mutation = '''
mutation{
    changeUserRole(email:"test1@emr.com", roleId: 1){
        user{
            name
            roles{
                role
            }
        }
    }
}
'''

change_user_role_with_already_assigned_role_mutation_response = "This role is already assigned to this user"  # noqa: E501

change_user_role_to_non_existence_role_mutation = '''
mutation{
  createUserRole(userId: 1, roleId: 10){
    userRole{
      id
      roles{
        id
      }
    }
  }
}
'''

change_user_role_to_non_existing_role_mutation_response = "Role id does not exist"  # noqa: E501

send_invitation_to_existent_user_query = '''
mutation{
    inviteToemr(email: "test1@emr.com"){
        email

    }
}
'''

send_invitation_to_nonexistent_user_query = '''
mutation{
    inviteToemr(email: "test2@emr.com"){
        email
    }
}
'''

send_invitation_to_invalid_email = '''
mutation{
    inviteToemr(email: "test3@gmail.com"){
        email
    }
}
'''

send_invitation_to_existent_user_response = {
    "errors": [{
        "message": "User already joined emr",
        "path": ["inviteToemr"]
    }],
    "data": {
        "inviteToemr": null
    }
}


get_users_by_role = '''
query{
    users(page:1, perPage:1, roleId:1){
        users{
            name
        }
    }
}
'''
get_user_by_role_reponse = {
    'data': {
        'users': {
            'users': [
                {
                    'name': 'Test User'
                }
            ]
        }
    }
}

change_role_of_non_existing_user_mutation = '''
mutation{
  changeUserRole(email:"someuser@emr.com", roleId:1){
    user{
      email
      roles{
        id
      }
    }
  }
}
'''

assign_role_to_non_existing_user_mutation = '''
mutation{
  createUserRole(userId: 100, roleId: 1){
    userRole{
      email
    }
  }
}
'''

query_user_by_name = '''
    query{
        userByName(userName:"Test User"){
            name
            email
        }
    }
'''

query_user_by_name_response = {
    'data': {
        'userByName': [{
            'name': 'Test User',
            'email': 'test.user@emr.com'
        }]
    }
}

query_non_existing_user_by_name = '''
    query{
        userByName(userName:"unknown user"){
            name
            email
        }
    }
'''

query_non_existing_user_by_name_response = {
    "errors": [
        {
            "message": "User not found",
            "path": [
                "userByName"
            ]
        }
    ],
    "data": {
        "userByName": null
    }
}
