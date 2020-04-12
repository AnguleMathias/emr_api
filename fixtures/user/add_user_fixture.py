null = None
invalid_email_mutation = '''
mutation {
  createUser(email: "mrm.com"
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

invalid_email_mutation_response = {
    "errors": [
        {
            "message": "This email is not allowed",
            "path": [
                "createUser"
            ]
        }
    ],
    "data": {
        "createUser": null
    }
}
