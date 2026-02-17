"""Context for portal nav: current user and role."""
def portal_nav(request):
    return {
        'portal_user': getattr(request, 'user', None) if request.user.is_authenticated else None,
    }
