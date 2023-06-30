from django.urls import path
from viewflow.contrib.auth import AuthViewset
from viewflow.urls import Application, Site, ModelViewset
from viewflow.workflow.flow import FlowAppViewset
from .flows import HelloWorldFlow


site = Site(title="ACME Corp", viewsets=[
    Application(
        title='Sample App', icon='people', app_name='sample', viewsets=[
            FlowAppViewset(HelloWorldFlow, icon="assignment"),
        ]
    ),
])

urlpatterns = [
    path('accounts/', AuthViewset(with_profile_view=False).urls),
    path('', site.urls),
]
