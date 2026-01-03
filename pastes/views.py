from rest_framework.views import APIView
from .models import Paste
from .serializers import CreatePasteSerializer, PasteResponseSerializer, PasteDetailSerializer
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from django.utils import timezone
from django.conf import settings
from django.db import connection
import datetime


def get_current_time(request):
    if settings.TEST_MODE and 'x-test-now-ms' in request.headers:
        try:
            timestamp_ms = int(request.headers['x-test-now-ms'])
            return datetime.datetime.fromtimestamp(
                timestamp_ms / 1000.0,
                tz=timezone.utc
            )
        except (ValueError, OSError):
            pass
        
    return timezone.now()

class HealthCheckView(APIView):
    # GET api/healthz
    
    def get(self, request):
        try:
            # Test DB connection
            connection.ensure_connection()
            return Response({"ok": True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"ok": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

class CreatePasteView(APIView):
    """POST /api/pastes"""
    
    def post(self, request):
        serializer = CreatePasteSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create paste
        paste = Paste.objects.create(
            content=serializer.validated_data['content'],
            ttl_seconds=serializer.validated_data.get('ttl_seconds'),
            max_view=serializer.validated_data.get('max_view')
        )
        
        # Build URL
        frontend_url = request.headers.get('Origin', 'http://localhost:3000')
        paste_url = f"{frontend_url}/p/{paste.id}"
        
        response_data = {
            "id": str(paste.id),
            "url": paste_url
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)
    

class FetchPasteView(APIView):
    # GET api/paste/id
    
    def get(self, request, id):
        try:
            paste = Paste.objects.get(pk=id)
        except Paste.DoesNotExist:
            return Response({'error': 'Paste not found'}, status=status.HTTP_404_NOT_FOUND)
        
        current_time = get_current_time(request)
        
        if not paste.is_available(current_time):
            return Response({'error': 'Paste not available'}, status=status.HTTP_404_NOT_FOUND)
        
        paste.increment_view_count()
        
        if not paste.is_available(current_time):
            return Response({'error': 'Paste not found'}, status=status.HTTP_404_NOT_FOUND)
        
        response_data = {
            'content': paste.content,
            'remaining_views': paste.get_remaining_views(),
            'expires_at': paste.get_expires_at()
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    

# def view_paste_html(request, id):
#     # GET /p/:id - HTML view
#     try:
#         paste = Paste.objects.get(pk=id)
#     except Paste.DoesNotExist:
#         return Response({'error': 'Paste not found'}, status=status.HTTP_404_NOT_FOUND)
    
#     current_time = get_current_time(request)
    
#     if not paste.is_available(current_time):
#         return render(request, '404.html', status=status.HTTP_404_NOT_FOUND)
    
#     context = {
#         'content': paste.content,
#         'paste_id': paste.id,
#     }
    
#     return render(request, 'paste_view.html', context)