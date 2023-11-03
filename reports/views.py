from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from projects.models import Project


class ProjectReport(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'projects.view_project'
    context_object_name = "project"
    template_name = 'reports/project_report.html'

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Project, pk=pk)


