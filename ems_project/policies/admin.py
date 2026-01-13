from django.contrib import admin
from .models import Policy

@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ['title', 'policy_type', 'version', 'effective_date', 'is_active', 'created_at']
    list_filter = ['policy_type', 'is_active', 'effective_date']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
