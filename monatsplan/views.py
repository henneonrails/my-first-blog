from django.views.generic import TemplateView

class MonatsplanView(TemplateView):
    template_name = "monatsplan/today.html"


