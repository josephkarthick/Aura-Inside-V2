from django.contrib import admin
from django.urls import path, include
from Accounts.views import login_view
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect


urlpatterns = [

    path('admin/', admin.site.urls),
    path('', lambda request: redirect('intranet/')),
    # Login paths
    path('login/', login_view, name='root-login'),
    path('accounts/', include('Accounts.urls')),

    # App URLs
    path('intranet/', include('Intranet.urls')),
    path('itdesk/', include('ITDesk.urls')),
    path('hrdesk/', include('HRDesk.urls')),
    path('admanager/', include('ADManager.urls')),
    path('auravoice/', include('auravoice.urls')),
    path('employee/', include('Employee.urls')),
   
    path('dashboard/', include('Dashboard.urls')),
    
    path("vault/", include("PasswordVault.urls")),
    
    path("books/", include("aura_books.urls")),
    
    path('maintenance/', include('Layout_Master.urls')),

    path(
        "intranet/layout-master/",
        include("Layout_Master.urls"),
    ),
    
    path("interactions/", include("interactions.urls")),
    
    path('assessment/',    include('Assessment.urls')), 
    
    path("IJP/", include("IJP.urls")),  
    
    path("cdr/", include("CDR.urls")),
    
    path("spaceview/", include("SpaceView.urls")),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
