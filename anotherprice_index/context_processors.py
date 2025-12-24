def member_login(request):
    return {
        'isMember': request.user.is_authenticated,
    }
