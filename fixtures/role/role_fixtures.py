null = None

role_mutation_query = '''
mutation {
  createRole(role:"dev"){
    role {
      role
    }
  }
}
'''

role_mutation_response = {
    "data": {
        "createRole": {
            "role": {
                "role": "dev"
            }
        }
    }
}

role_duplication_mutation_response = {
    "errors": [
        {
            "message": "dev Role already exists",
            "path": [
                "createRole"
            ]
        }
    ],
    "data": {
        "createRole": null
    }
}

role_query = '''
query {
  roles {
    role
  }
}
'''

role_query_response = {
    "data": {
        "roles": [
            {
                "role": "Admin"
            },
            {
                "role": "Test"
            },
            {
                "role": "Doctor"
            },
        ]
    }
}

query_role_by_role = '''
 query {
  role(role: "Ops"){
    role
  }
}
'''

query_role_by_role_response = {
    "data": {
        "role": {
            "role": "Ops"
        }
    }
}
