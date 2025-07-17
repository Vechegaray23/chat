class ValidationError(Exception):
    pass

def validate(instance, schema):
    if not isinstance(instance, dict):
        raise ValidationError("Instance must be an object")
    if 'title' not in instance or not isinstance(instance['title'], str):
        raise ValidationError('Missing or invalid title')
    if 'questions' not in instance or not isinstance(instance['questions'], list):
        raise ValidationError('Missing or invalid questions')
    for q in instance['questions']:
        if not isinstance(q, dict):
            raise ValidationError('Invalid question')
        for field in ('id', 'type', 'text'):
            if field not in q:
                raise ValidationError(f'Missing {field}')
        if q['type'] not in {'single_choice', 'multiple_choice', 'text'}:
            raise ValidationError('Invalid question type')
