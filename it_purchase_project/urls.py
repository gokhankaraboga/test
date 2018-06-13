from django.conf.urls import include, url, re_path
from django.contrib.auth import views as auth
from material.frontend.registry import modules
from material import frontend
from material.frontend.apps import ModuleMixin
from django.views import generic
from django.views.generic import RedirectView
from django.conf.urls.i18n import i18n_patterns


class Purchase(ModuleMixin):
    """
    Home page module
    """
    order = 1
    label = 'Introduction'
    icon = '<i class="material-icons">account_balance</i>'

    @property
    def urls(self):
        index_view = generic.TemplateView.as_view(
template_name='it_purchase_app/index.html')

        return frontend.ModuleURLResolver(
            '^', [url('^$', index_view, name="index")],
            module=self, app_name='it_purchase_app',
namespace='it_purchase_app')

    def index_url(self):
        return '/'

    def installed(self):
        return True


modules.register(Purchase())


from material.frontend import urls as frontend_urls  # NOQA


urlpatterns = [
    url(r'^login/$', auth.login, name='login'),
    url(r'^logout/$', auth.logout, name='logout'),
    url(r'^$', generic.RedirectView.as_view(url='/workflow/', permanent=False)),
    url(r'', include(frontend_urls)),
    re_path('i18n/', include('django.conf.urls.i18n')),
    #url(r'^', include('it_purchase_project.profile.urls')),

]
