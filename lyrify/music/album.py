from lyrify.utils.functions import log_function

class Album:
    def __init__(self, title=None, artist=None, release_date=None, number_of_tracks=1):
        self.title = title
        self.artist = artist
        self.release_date = release_date
        self.number_of_tracks = number_of_tracks
        self.songs = []
        
    @log_function('Album Information', ' ')
    def log_info(self):
        print('Artist:', self.artist)
        print('Album:', self.title)
        print('Release date:', self.release_date)
        print('Number of tracks:', self.number_of_tracks)
        print('\nTracks:')
        for song in self.songs:
            print(f'{song.track_number:02d} - {song.title}')
        
    def add_song(self, song):
        self.songs.append(song)
        
    def get_number_of_tracks(self):
        return len(self.songs)
    
    def set_songs_release_date(self):
        for song in self.songs:
            song.release_date = self.release_date
    
    def set_songs_artist(self):
        for song in self.songs:
            song.artist = self.artist
    
    def set_songs_album(self):
        for song in self.songs:
            song.album = self.title