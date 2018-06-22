from django.conf.urls import include, url, re_path
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth
from django.views import generic
from material import frontend
from material.frontend.apps import ModuleMixin
from material.frontend.registry import modules


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
            template_name='../templates/material/frontend/base_site.html')

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
    re_path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(url(r'', include(frontend_urls)),
                             url(r'^login/$', auth.login, name='login'),
                             url(r'^logout/$', auth.logout, name='logout'),
                             )
