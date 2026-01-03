from django.db import models
from django.utils import timezone
import uuid

# Create your models here.
class Paste(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=56,
        default=uuid.uuid4,
        editable=False
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    ttl_seconds = models.IntegerField(null=True, blank=True)
    max_view = models.IntegerField(null=True, blank=True)
    view_count = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'pastes'
        indexes = [
            models.Index(fields=['created_at'])
        ]
        
    def is_expired(self, current_time=None):
        # Check paste has expired based on TTL
        if not self.ttl_seconds:
            return False
        
        if current_time is None:
            current_time = timezone.now()
        
        expiry_time = self.created_at + timezone.timedelta(seconds=self.ttl_seconds)
        return current_time >= expiry_time
    
    def is_view_limit_exceeded(self):
        if not self.max_view:
            return False    
        return self.view_count >= self.max_view
    
    
    def is_available(self, current_time=None):
        # Check the paste is still available
        return not (self.is_expired(current_time) or self.is_view_limit_exceeded())
    
    def get_expires_at(self):
        if not self.ttl_seconds:
            return None
        return self.created_at + timezone.timedelta(seconds=self.ttl_seconds)
    
    def get_remaining_views(self):
        if not self.max_view:
            return None
        return max(0, self.max_view - self.view_count)
    
    def increment_view_count(self):
        from django.db.models import F
        Paste.objects.filter(pk=self.pk).update(view_count=F('view_count') + 1)
        return self.refresh_from_db()