from django.apps import apps
from django.core.paginator import Paginator
from django.contrib import auth

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
# from rest_framework.pagination import PaginationSerializer
# from rest_framework import pagination

# import tracks.models as Track
# from tracks.models import Track
# from artists.models import Artist

# from .models import Album

 
Track = apps.get_model(app_label='tracks', model_name='Track')
Artist = apps.get_model(app_label='artists', model_name='Artist')
Album = apps.get_model(app_label='albums', model_name='Album')
# Like = apps.get_model(app_label='likes', model_name='Like')
Image = apps.get_model(app_label='images', model_name='Image')


class ArtistsSerializer(serializers.ModelSerializer):

    id = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = [
            'id',
            'name',
            'artist_uri',

        ]
        ref_name = "AlbumArtist"

    def get_id(self, obj):

        return obj.artist_uri

class AlbumImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = [
            # 'id',
            'url',
            'height',
            'width',

        ]


class TrackSerializer(serializers.ModelSerializer):
    artists = ArtistsSerializer(many=True)
    # is_liked = serializers.SerializerMethodField()
    # total_likes = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    class Meta:
        model = Track
        fields = [
            'id',
            'name',
            'artists',
            'track_uri',
            'track_number',

            # 'is_liked',
            # 'likes_count',
            # 'total_likes',
        ]
        # depth = 2

    def get_id(self, obj):

        return obj.track_uri

    def get_is_liked(self, obj):

        # user = self.context.get('request').user
        user = self.context['request'].user
        return likes_services.is_fan(obj, user)

    def get_total_likes(self, obj):
        return likes_services.get_object_likes_count(obj)


class AlbumsSerializer(serializers.ModelSerializer):
    artists = ArtistsSerializer(many=True)
    tracks = serializers.SerializerMethodField()
    images = AlbumImagesSerializer(many=True)
    is_liked = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    # posts = PostsSerializer(many=True)


    class Meta:
        model = Album
        fields = [
            'pk',
            'id',
            'name',
            'is_liked',
            'total_likes',

            'tracks',
            'artists',
            # 'images',
            # 'album_id',
            'album_uri',
            'images',

            # 'likes_count',

            'created_at',
            'updated_at',
            # 'likes_count',
        ]
        # depth = 2

    def get_id(self, obj):

        return obj.album_uri

    def get_tracks(self, obj):
        serializer = TrackSerializer(obj.tracks, many=True).data
        data = Paginator(obj.tracks, 2)


        # serialize = pagination.PaginationSerializer(instance=page)
        # serialize.data
        return {
            'href': 'https://ardegraph.com/albums/:id/tracks?offset=0&limit=50',
            'items': serializer,
            'count': data.count,
            'num_pages': data.num_pages,
            # 'next': data.get_next_link(),
            # 'next': self.get_next_link(),
            # 'previous': data.get_previous_link(),
            # ''
        }
        # return  serialize.data

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        # user = self.context['request'].user
        return likes_services.is_fan(obj, user)

    def get_total_likes(self, obj):
        return likes_services.get_object_likes_count(obj)
