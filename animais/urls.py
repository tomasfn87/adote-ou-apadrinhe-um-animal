from django.urls import path

from . import views

app_name = "animais"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("cadastro/", views.cadastro, name="cadastro"),
    path("cadastro/sucesso/", views.cadastro_sucesso, name="cadastro_sucesso"),
    path("sobre/", views.SobreView.as_view(), name="sobre"),
    path("login/", views.login_admin , name="login_admin"),
    path("logout/", views.logout_admin , name="logout_admin"),
    path("registro_doacao/", views.registro_doacao , name="registro_doacao"),
    path("delete_doacao/<int:doacao_id>", views.delete_doacao , name="delete_doacao"),
    path("metas/", views.metas , name="metas"),
    path("delete_meta/<int:meta_id>", views.delete_meta , name="delete_meta"),
    path("status_meta/", views.status_meta , name="status_meta"),
]