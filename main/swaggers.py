from drf_yasg import openapi
# view request schema
mbti_view_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'answer': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            additionalProperties=openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='Question id'
            ),
            description='Option id'
        )
    },
    required=['answer']
)

# view response schema
question_view_schema = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Qustion id'),
            'text': openapi.Schema(type=openapi.TYPE_STRING, description='Question text'),
            'options': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Option id'),
                        'text': openapi.Schema(type=openapi.TYPE_STRING, description='Option text'),
                    }
                ),
                description='Options for Qustion'
            )
        }
    )
)

mbti_view_schema = schema=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'mbti': openapi.Schema(type=openapi.TYPE_STRING, description='MBTI'),
        'text': openapi.Schema(type=openapi.TYPE_STRING, description='MBTI description')
    }
)

# error response schema
status_400_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'error': openapi.Schema(
            type=openapi.TYPE_STRING, description='400 error message'
        )
    }
)

status_500_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'error': openapi.Schema(
            type=openapi.TYPE_STRING, description='500 error message'
        )
    }
)