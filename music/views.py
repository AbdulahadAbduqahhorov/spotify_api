from django.contrib.postgres.search import TrigramSimilarity
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from music.models import Song, Album,Artist
from music.serializers import SongSerializer, AlbumSerializer,ArtistSerializer


# class SongsAPIView(APIView):
#     def get(self,request):
#         songs = Song.objects.all()
#         serializer = SongSerializer(songs,many=True)
#
#         return Response(data=serializer.data)
#     def post(self,request):
#         serializer = SongSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         serializer.save()
#
#         return Response(data=serializer.data)

class SongViewSet(ReadOnlyModelViewSet):
    serializer_class = SongSerializer
    queryset = Song.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["listened","-listened"]
    # search_fields = ["title","album__artist__name","album__title"]


    def get_queryset(self):
        queryset = Song.objects.all()
        query = self.request.query_params.get('search')
        if query is not None:
            queryset = Song.objects.annotate(
                similarity=TrigramSimilarity('title',query)).filter(similarity__gt=0.).order_by('-similarity')

        return queryset


    @action(detail=True,methods=["POST"])
    def listen(self,request,*args,**kwargs):
        song = self.get_object()
        with atomic():
            song.listened += 1
            song.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,methods=['GET'])
    def top(self,request,*args,**kwargs):
        songs = self.get_queryset()
        songs = songs.order_by('-listened')[:10]
        serializer = SongSerializer(songs,many=True)
        return Response(serializer.data)



class AlbumViewSet(ReadOnlyModelViewSet):
    serializer_class = AlbumSerializer
    queryset = Album.objects.all()

class ArtistViewSet(ReadOnlyModelViewSet):
    serializer_class = ArtistSerializer
    queryset = Artist.objects.all()

    @action(detail=True,methods=['GET'])
    def albums(self,request,*args,**kwargs):
        artist = self.get_object()
        serializer = AlbumSerializer(artist.album_set.all(),many=True)

        return Response(serializer.data)


