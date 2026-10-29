from django.contrib import admin
from .models import Survey, Response, Answer, RecognitionPoster

admin.site.register(Survey)
admin.site.register(Response)
admin.site.register(Answer)
admin.site.register(RecognitionPoster)
