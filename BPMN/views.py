from django import forms
from django.views.generic import TemplateView
from viewflow import flow, frontend
from viewflow.base import this, Flow
from viewflow.flow.views import StartFlowMixin
from .models import GreetingProcess


class GreetingForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)


class GreetingFlow(Flow):
    process_class = GreetingProcess
    start = flow.Start(StartFlowMixin, GreetingForm) \
        .Next(this.greet)

    greet = flow.View(TemplateView) \
        .Assign(lambda act: act.process.hello()) \
        .Next(this.end)

    end = flow.End()

    def hello(self):
        self.process.name = self.activation.cleaned_data['name']
        self.process.save()

    def get_task_title(self, task):
        return 'Hello, {0}!'.format(task.process.name)


class GreetingProcess(flow.Process):
    name = flow.CharField(label='Your name', max_length=100)

    def hello(self):
        print('Hello, {0}!'.format(self.name))


frontend.register(GreetingFlow)