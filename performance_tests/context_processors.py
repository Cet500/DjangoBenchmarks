def user_theme(request):
    return {
        'hue': request.session.get('user_theme_hue', 215),
        'saturation': request.session.get('user_theme_saturation', 100),
    }
