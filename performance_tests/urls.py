from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('test_results', views.TestResultViewSet, basename='test_result')


urlpatterns = [
    path( '', views.index, name='index' ),
    path( 'settings/accent_color', views.settings_color, name='settings_color' ),

    path( 'info/results',  views.test_results,  name='test_results' ),
    path( 'info/server',   views.server_info,   name='server_info'  ),
    path( 'info/charts',   views.charts,        name='charts'       ),

    path( 'test/math/pi/<int:digits>',           views.pi_calculation,    name='pi_calculation'  ),
    path( 'test/math/matrix/<int:size>',         views.matrix_mult,       name='matrix_mult'     ),
    path( 'test/math/primes/<int:count>',        views.generate_primes,   name='generate_primes' ),
    path( 'test/math/factorial/<int:n>',         views.calc_factorial,    name='calc_factorial'  ),
    path( 'test/math/fibonacci/<int:n>',         views.calc_fibonacci,    name='calc_fibonacci'  ),
    path( 'test/math/power/<int:a>/<int:b>',     views.calc_power,        name='calc_power'      ),
    path( 'test/math/partitions/<int:n>',        views.calc_partitions,   name='calc_partitions' ),
    path( 'test/math/list_permutations/<int:n>', views.list_permutations, name='list_permutations' ),

    path('api/', include(router.urls)),
]
