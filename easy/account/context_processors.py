from django.conf import settings

from .models import Account, AnonymousAccount


def account(request):
    if request.user.is_authenticated():
        try:
            account = Account._default_manager.get(user=request.user)
        except Account.DoesNotExist:
            if getattr(settings, 'ANONYMOUS_USER_ACCOUNTS', None):
                account = Account.create(user_id=0, id=Account.find_id_from_request(req))
            else:
                account = AnonymousAccount(request)
    else:
        account = AnonymousAccount(request)
    return {
        "account": account,
        "CONTACT_EMAIL": getattr(settings, "CONTACT_EMAIL", "support@example.com")
    }
