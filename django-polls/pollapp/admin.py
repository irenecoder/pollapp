from django.contrib import admin
from pollapp.models import Question,Choice

# Register your models here.

# admin.site.register(Choice)
class ChoiceInLine(admin.TabularInline):
    model =Choice
    extra = 3 

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['quiz_text']}),
        ('Date information', {'fields': ['date_created'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInLine ]
    list_display = ('quiz_text','date_created','was_published_recently')
    list_filter = ['date_created']
    search_fields = ['quiz_text']
   
admin.site.register(Question,QuestionAdmin)
