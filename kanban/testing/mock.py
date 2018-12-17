"""
UAMS測資mock
"""

class Request():
    """偽裝Django的request和session"""
    def __init__(self):
        from django.http import HttpRequest
        from KB import settings as st
        from django.conf import settings
        settings.configure(
            DEBUG=True,
            TEMPLATE_DEBUG=True,
            DATABASES=st.DATABASES,
            INSTALLED_APPS=st.INSTALLED_APPS,
            MIDDLEWARE_CLASSES=st.MIDDLEWARE_CLASSES
        )
        from django.contrib.sessions.middleware import SessionMiddleware
        self.request = HttpRequest()
        middleware = SessionMiddleware()
        middleware.process_request(self.request)

    def generate(self):
        return self.request
