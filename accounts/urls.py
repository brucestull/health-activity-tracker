from django.urls import path

from accounts import views

urlpatterns = [
    # Try to override 'login' view.
    path("login/", views.CustomLoginView.as_view(), name="login"),

    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("dashboard/", views.UserDashboardView.as_view(), name="dashboard"),
    path("<int:pk>/edit/", views.UserUpdateView.as_view(), name="edit_profile"),
]