# admin.py
from django.contrib import admin
from .models import URLHistory
class URLHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'url', 'result', 'timestamp')  # Columns to display
    search_fields = ('user__username', 'url')  # Allow searching by username and URL
    list_filter = ('result', 'timestamp')  # Filters for result and timestamp

# Register with the custom admin class
admin.site.register(URLHistory, URLHistoryAdmin)
