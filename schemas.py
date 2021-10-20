user_insert_schema = {
    'type': 'object',
    'required': ['fullname', 'email', 'liste_quartiers', 'password'],
    'properties': {
        'fullname': {
            'type': 'string'
        },
        'email': {
            'type': 'string'
        },
        'liste_quartiers': {
            'type': 'array',
            'items': {
                'type': 'string'
            }
        },
        'password': {
            'type': 'string'
        },
        'picture': {
            'type': 'string',
            'media': {
                'binaryEncoding': 'base64',
                'type': ['image/png', 'image/jpeg']
            }
        }
    },
    'additionalProperties': False
}

user_update_schema = {
    'type': 'object',
    'required': ['fullname', 'email', 'liste_quartiers', 'password', 'id'],
    'properties': {
        'id': {
            'type': 'number'
        },
        'fullname': {
            'type': 'string'
        },
        'email': {
            'type': 'string'
        },
        'liste_quartiers': {
            'type': 'array',
            'items': {
                'type': 'string'
            }
        },
        'picture': {
            'type': 'string',
            'media': {
                'binaryEncoding': 'base64',
                'type': ['image/png', 'image/jpeg']
            }
        }
    },
    'additionalProperties': False
}
