from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from .models import Track


def tracks_list(request):
    """
    Return all tracks as JSON with pagination
    """
    try:
        # Get pagination parameters
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 20)  # Default 20 items per page

        # Validate page_size (max 100)
        try:
            page_size = int(page_size)
            if page_size > 100:
                page_size = 100
            elif page_size < 1:
                page_size = 20
        except (ValueError, TypeError):
            page_size = 20

        tracks = Track.objects.all().order_by('id')  # Consistent ordering for pagination

        # Create paginator
        paginator = Paginator(tracks, page_size)

        try:
            paginated_tracks = paginator.page(page)
        except PageNotAnInteger:
            paginated_tracks = paginator.page(1)
        except EmptyPage:
            paginated_tracks = paginator.page(paginator.num_pages)

        # Convert tracks to list of dictionaries
        tracks_data = []
        for track in paginated_tracks:
            track_dict = {
                'id': track.id,
                's3_key': track.s3_key,
                # Add other fields from your Track model as needed
                # 'title': track.title,
                # 'artist': track.artist,
                # 'duration': track.duration,
                # 'created_at': track.created_at.isoformat() if hasattr(track, 'created_at') else None,
                # 'updated_at': track.updated_at.isoformat() if hasattr(track, 'updated_at') else None,
            }
            tracks_data.append(track_dict)

        return JsonResponse({
            'status': 'success',
            'data': tracks_data,
            'pagination': {
                'current_page': paginated_tracks.number,
                'total_pages': paginator.num_pages,
                'total_items': paginator.count,
                'page_size': page_size,
                'has_next': paginated_tracks.has_next(),
                'has_previous': paginated_tracks.has_previous(),
                'next_page': paginated_tracks.next_page_number() if paginated_tracks.has_next() else None,
                'previous_page': paginated_tracks.previous_page_number() if paginated_tracks.has_previous() else None,
            }
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def track_detail(request, track_id):
    """
    Return a single track by ID
    """
    try:
        track = Track.objects.get(id=track_id)

        track_data = {
            'id': track.id,
            's3_key': track.s3_key,
            # Add other fields as needed
        }

        return JsonResponse({
            'status': 'success',
            'data': track_data
        })

    except Track.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Track not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


# Alternative approach using Django's built-in serializers with pagination
def tracks_list_serialized(request):
    """
    Alternative implementation using Django's serializers with pagination
    """
    try:
        # Get pagination parameters
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 20)

        # Validate page_size (max 100)
        try:
            page_size = int(page_size)
            if page_size > 100:
                page_size = 100
            elif page_size < 1:
                page_size = 20
        except (ValueError, TypeError):
            page_size = 20

        tracks = Track.objects.all().order_by('id')

        # Create paginator
        paginator = Paginator(tracks, page_size)

        try:
            paginated_tracks = paginator.page(page)
        except PageNotAnInteger:
            paginated_tracks = paginator.page(1)
        except EmptyPage:
            paginated_tracks = paginator.page(paginator.num_pages)

        # Use Django's serializers
        tracks_json = serializers.serialize('json', paginated_tracks)
        tracks_data = json.loads(tracks_json)

        # Extract just the fields we need
        simplified_data = []
        for item in tracks_data:
            simplified_data.append({
                'id': item['pk'],
                **item['fields']  # This includes s3_key and other model fields
            })

        return JsonResponse({
            'status': 'success',
            'data': simplified_data,
            'pagination': {
                'current_page': paginated_tracks.number,
                'total_pages': paginator.num_pages,
                'total_items': paginator.count,
                'page_size': page_size,
                'has_next': paginated_tracks.has_next(),
                'has_previous': paginated_tracks.has_previous(),
                'next_page': paginated_tracks.next_page_number() if paginated_tracks.has_next() else None,
                'previous_page': paginated_tracks.previous_page_number() if paginated_tracks.has_previous() else None,
            }
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


# CORS-enabled view for React frontend
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

@method_decorator(csrf_exempt, name='dispatch')
class TracksAPIView(View):
    """
    Class-based view with CORS support for React
    """

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)

        # Add CORS headers
        response['Access-Control-Allow-Origin'] = '*'  # In production, specify your React app's domain
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'

        return response

    def options(self, request, *args, **kwargs):
        """Handle preflight requests"""
        response = JsonResponse({})
        return response

    def get(self, request, *args, **kwargs):
        """Get all tracks with pagination"""
        try:
            # Get pagination parameters
            page = request.GET.get('page', 1)
            page_size = request.GET.get('page_size', 20)

            # Validate page_size (max 100)
            try:
                page_size = int(page_size)
                if page_size > 100:
                    page_size = 100
                elif page_size < 1:
                    page_size = 20
            except (ValueError, TypeError):
                page_size = 20

            tracks = Track.objects.all().order_by('id')

            # Create paginator
            paginator = Paginator(tracks, page_size)

            try:
                paginated_tracks = paginator.page(page)
            except PageNotAnInteger:
                paginated_tracks = paginator.page(1)
            except EmptyPage:
                paginated_tracks = paginator.page(paginator.num_pages)

            tracks_data = []
            for track in paginated_tracks:
                track_dict = {
                    'id': track.id,
                    's3_key': track.s3_key,
                    # Add other fields as needed
                }
                tracks_data.append(track_dict)

            return JsonResponse({
                'status': 'success',
                'data': tracks_data,
                'pagination': {
                    'current_page': paginated_tracks.number,
                    'total_pages': paginator.num_pages,
                    'total_items': paginator.count,
                    'page_size': page_size,
                    'has_next': paginated_tracks.has_next(),
                    'has_previous': paginated_tracks.has_previous(),
                    'next_page': paginated_tracks.next_page_number() if paginated_tracks.has_next() else None,
                    'previous_page': paginated_tracks.previous_page_number() if paginated_tracks.has_previous() else None,
                }
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
