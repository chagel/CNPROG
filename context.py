from django.conf import settings
def application_settings(context):
    return {
        'APP_TITLE' : settings.APP_TITLE,
        'APP_URL'   : settings.APP_URL,
        'APP_KEYWORDS' : settings.APP_KEYWORDS,
        'APP_DESCRIPTION' : settings.APP_DESCRIPTION,
        'APP_INTRO' : settings.APP_INTRO
        }
