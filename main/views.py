from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from application.models import Proposal



# def home_view(request):
#     return render(request, 'main/home.html')

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "main/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        applicant = self.request.user
        context['applicant'] = applicant

        try:
            context['proposals'] = Proposal.objects.get(applicant=applicant)
        except Proposal.DoesNotExist:
            context['proposals'] = None

        return context