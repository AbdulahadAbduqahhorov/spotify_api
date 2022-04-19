from django.test import TestCase
import pytest
from music.models import Artist, Album
from music.serializers import ArtistSerializer, SongSerializer

pytestmark = pytest.mark.django_db

TEST_DATABASE_PREFIX = 'test_'


class TestArtistSerializer(TestCase):
    def setUp(self) -> None:
        self.artist = Artist.objects.create(name="Example artist")

    def test_data(self):
        data = ArtistSerializer(self.artist).data
        assert data["id"] != None
        assert data['name'] == "Example artist"
        assert data['picture'] == ''


class TestSongSerializer(TestCase):
    def setUp(self) -> None:
        self.artist = Artist.objects.create(name="Test artist")
        self.album = Album.objects.create(artist=self.artist, title="Test album")

    def test_is_valid(self):
        data = {
            "title": "Test song",
            'album': self.album.id, 'cover': '',
            'source': 'http://example.com/music.mp3',
            'listened': 0
        }
        serializer = SongSerializer(data=data)
        assert serializer.is_valid() == True
        # print(serializer.errors)

    def test_is_not_valid(self):
        data = {
            "title": "Test song",
            'album': self.album.id, 'cover': '',
            'source': 'http://example.com/music',
            'listened': 0
        }
        serializer = SongSerializer(data=data)
        assert serializer.is_valid() == False
        assert str(serializer.errors['source'][0]) == ' mp3 file required'
