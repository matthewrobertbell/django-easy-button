from django.conf import settings
from django.conf.urls.defaults import *

from .forms import SignupForm


if settings.ACCOUNT_OPEN_SIGNUP:
    signup_view = "easy.account.views.signup"
else:
    if getattr(settings, 'OPEN_WAITING_LIST', False):
        signup_view = "easy.waitinglist.views.list_signup"
    else:
        signup_view = "easy.signup_codes.views.signup"


urlpatterns = patterns("",
    url(r"^email/$", "easy.account.views.email", name="acct_email"),
    url(r"^signup/$", signup_view, name="acct_signup"),
    url(r"^login/$", "easy.account.views.login", name="acct_login"),
    url(r"^login/openid/$", "easy.account.views.login", {"associate_openid": True},
        name="acct_login_openid"),
    url(r"^password_change/$", "easy.account.views.password_change", name="acct_passwd"),
    url(r"^password_set/$", "easy.account.views.password_set", name="acct_passwd_set"),
    url(r"^password_delete/$", "easy.account.views.password_delete", name="acct_passwd_delete"),
    url(r"^password_delete/done/$", "django.views.generic.simple.direct_to_template", {
        "template": "account/password_delete_done.html",
    }, name="acct_passwd_delete_done"),
    url(r"^timezone/$", "easy.account.views.timezone_change", name="acct_timezone_change"),
    url(r"^other_services/$", "easy.account.views.other_services", name="acct_other_services"),
    url(r"^other_services/remove/$", "easy.account.views.other_services_remove", name="acct_other_services_remove"),
    
    url(r"^language/$", "easy.account.views.language_change", name="acct_language_change"),
    url(r"^logout/$", "django.contrib.auth.views.logout", {"template_name": "account/logout.html"}, name="acct_logout"),
    
    url(r"^confirm_email/(\w+)/$", "emailconfirmation.views.confirm_email", name="acct_confirm_email"),
    
    # password reset
    url(r"^password_reset/$", "easy.account.views.password_reset", name="acct_passwd_reset"),
    url(r"^password_reset/done/$", "easy.account.views.password_reset_done", name="acct_passwd_reset_done"),
    url(r"^password_reset_key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$", "easy.account.views.password_reset_from_key", name="acct_passwd_reset_key"),
    
    # ajax validation
    (r"^validate/$", "ajax_validation.views.validate", {"form_class": SignupForm}, "signup_form_validate"),
)
