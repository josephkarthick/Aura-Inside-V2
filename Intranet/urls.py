from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    home,
    org_chart,
    admin_org_chart,
    add_board_member,
    delete_board_member,
    edit_board_member,
    admin_list_content,
    add_home_content,
    edit_home_content,
    delete_home_content,
    gallery,
    upload_images,
    delete_image,
    aura_flag,
)

app_name = 'Intranet'

urlpatterns = [
    path('', home, name='home'),
    path('orgchart/', org_chart, name='org_chart'), 
    path('add_board_member/',add_board_member, name='add_board_member'),
    path('admin_org_chart/', admin_org_chart, name='admin_org_chart'),     
    path('delete_board_member/<str:member_id>/', delete_board_member, name='delete_board_member'),
    path('edit_board_member/', edit_board_member, name='edit_board_member'),
    path('admin_list_content/', admin_list_content, name='admin_list_content'),
    path('add_home_content', add_home_content, name='add_home_content'),
    path('edit_home_content', edit_home_content, name='edit_home_content'),
    path('delete_home_content/<int:item_id>/', delete_home_content, name='delete_home_content'),
    path('gallery/', gallery, name='gallery'),
    path('upload/', upload_images, name='upload_images'),  
    path('flag/', aura_flag, name='flag'),     
    path("image/delete/<int:image_id>/", delete_image, name="delete_image"),    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


