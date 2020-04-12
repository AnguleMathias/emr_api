delete_user = '''
mutation {
    deleteUser(email: "new.user@emr.com") {
        user{
            id
            email
            roles {
                id
                role
            }
        }
    }
}
'''

delete_user_2 = '''
mutation {
    deleteUser(email: "test.test@emr.com") {
        user{
            email
            roles {
                role
            }
        }
    }
}
'''

mutation_hard_delete_user = '''
mutation {
    deleteUser(email: "test1@emr.com", remove: true) {
        user{
            email
            roles {
                role
            }
        }
    }
}
'''

expected_response_hard_delete_user = {
    "data": {
        "deleteUser": {
            "user": {
                "email": "test1@emr.com",
                "roles": [
                    {
                        "role": "Admin"
                    }
                ]
            }
        }
    }
}

delete_self = '''
mutation {
    deleteUser(email: "test2@emr.com") {
        user{
            id
            email
            roles {
                id
                role
            }
        }
    }
}
'''

user_not_found = '''
mutation {
    deleteUser(email: "test@emr.com") {
        user{
            id
            email
            roles {
                id
                role
            }
        }
    }
}
'''


expected_query_after_delete = {
    "data": {
        "deleteUser": {
            "user": {
                "email": "test.test@emr.com",
                "roles": [
                    {
                        "role": "Default User"
                    }
                ]
            }
        }
    }
}

expected_query_after_delete_for_admin = {
    "data": {
        "deleteUser": {
            "user": {
                "id": "2",
                "email": "new.user@emr.com",
                "roles": [
                    {
                        "id": "1",
                        "role": "Admin"
                    }
                ]
            }
        }
    }
}

user_invalid_email = '''
mutation {
    deleteUser(email: "useremrcom") {
        user{
            id
            email
            roles {
                id
                role
            }
        }
    }
}
'''
