from django.contrib import admin
from .models import Hospital_Information, Patient, User, ContactMessage

# ── Standard registrations ──
admin.site.register(User)
admin.site.register(Hospital_Information)
admin.site.register(Patient)


# ── ContactMessage — rich admin view ──
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ('name', 'email', 'phone', 'subject', 'city', 'short_message', 'created_at')
    list_filter   = ('subject', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'phone', 'subject', 'city', 'message', 'created_at')
    ordering      = ('-created_at',)
    date_hierarchy = 'created_at'

    # Show first 80 chars of message in list view
    def short_message(self, obj):
        return obj.message[:80] + ('...' if len(obj.message) > 80 else '')
    short_message.short_description = 'Message Preview'

    # Prevent accidental edits — messages should stay as-is
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False  # read-only; delete is still allowed
