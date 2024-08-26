from django.apps import apps

def get_all_custom_models_name():
    default_models = ['LogEntry', 'Permission', 'Group', 'User', 'ContentType', 'Session', 'Upload']
    custom_models = []
    for model in apps.get_models():
        name = model.__name__
        if name not in default_models:
            custom_models.append(name)
    return custom_models
