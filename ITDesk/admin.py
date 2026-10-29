from django.contrib import admin
from .models import Tkt_Cat,Tkt_SubCat,Priority_Choice,Renewal,RenewalHeading,AssetCategory,VoIPAPI

admin.site.register(Tkt_Cat)
admin.site.register(Tkt_SubCat)
admin.site.register(Priority_Choice)
admin.site.register(Renewal)
admin.site.register(RenewalHeading)
admin.site.register(AssetCategory)
admin.site.register(VoIPAPI)



