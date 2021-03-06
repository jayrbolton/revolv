from revolv.base.utils import ProjectGroup
from revolv.base.views import BaseStaffDashboardView
from revolv.project.models import Project


class AmbassadorDashboardView(BaseStaffDashboardView):
    """Basic view for the Ambassador dashboard.
    """
    template_name = 'base/dashboard.html'
    role = "ambassador"

    def get_filter_args(self):
        """
        Return a list that contains a set of projects that this user owns, to pass
        to various Project filtering functions.
        """
        return [Project.objects.owned_projects(self.user)]

    def get_context_data(self, **kwargs):
        context = super(AmbassadorDashboardView, self).get_context_data(**kwargs)
        context = super(AmbassadorDashboardView, self).get_context_data(**kwargs)
        context["donated_amount"] = self.request.session.get('amount')
        context["donated_project"] = self.request.session.get('project')
        context["cover_photo"] = self.request.session.get('cover_photo')
        context["url"] = self.request.session.get('url')
        context["social"] = self.request.session.get('social')
        if self.request.session.get('social'):
            del self.request.session['social']
        amount = self.user_profile.reinvest_pool + self.user_profile.solar_seed_fund_pool
        if self.user_profile and amount > 0.0:
            context["reinvestment_amount"] = self.user_profile.reinvest_pool + self.user_profile.solar_seed_fund_pool
        else:
            context["reinvestment_amount"] = 0.0
        context["project_dict"][ProjectGroup('Drafted Projects', "drafted")] = Project.objects.get_drafted(*self.get_filter_args())
        return context

