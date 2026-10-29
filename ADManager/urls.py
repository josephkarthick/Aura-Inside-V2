from django.urls import path
from .views import aduser, ad_user_detail, create_ldap_user, delete_ldap_user, export_ldap_users,adcomputers,export_computers_excel,sync_security_groups

app_name = "ADManager"

urlpatterns = [
    path('adusers/', aduser, name='aduser'),
    path('adusers/<str:username>/', ad_user_detail, name='ad_user_detail'),
    path('ldap/create-user/', create_ldap_user, name='create_ldap_user'),
    path('ldap/delete-user/<str:username>/', delete_ldap_user, name='delete_ldap_user'),
    path('export-users/<str:filetype>/', export_ldap_users, name='export_ldap_users'),
    path('adcomputers/', adcomputers, name="adcomputers"),
    path('export-computers/', export_computers_excel, name='export_computers_excel'),    
    
    path("sync-security-groups/",sync_security_groups,name="sync_security_groups"),
    
]
