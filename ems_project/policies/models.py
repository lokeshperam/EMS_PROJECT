from django.db import models
from django.conf import settings

class Policy(models.Model):
    POLICY_TYPES = [
        ('HR', 'HR Policy'),
        ('IT', 'IT Policy'),
        ('SECURITY', 'Security Policy'),
        ('COMPLIANCE', 'Compliance Policy'),
        ('OTHER', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    policy_type = models.CharField(max_length=20, choices=POLICY_TYPES, default='OTHER')
    document = models.FileField(upload_to='policies/', blank=True, null=True)
    content = models.TextField(blank=True)
    version = models.CharField(max_length=20, default='1.0')
    effective_date = models.DateField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='policies_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Policies'
    
    def __str__(self):
        return f"{self.title} (v{self.version})"
