from django.urls import path     
from . import views

urlpatterns = [
    path('', views.logIn),
    path('register', views.addRegistrations),
    path('login', views.addLogin),
    path('dashboard',views.pies),
    path('pies/add',views.addPies),
    path('pies/<int:pie_id>/update',views.updatePies),
    path('pies/delete',views.deletePies),
    path('piess',views.allPies),
    path('pies/<int:pie_id>/favorite', views.favoritePie),
    path('pies/<int:pie_id>/unfavorite', views.unfavoritePie),
    path('pies/<int:pie_id>', views.showPies),
    path('logout',views.logOut)

]