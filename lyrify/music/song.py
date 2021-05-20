
class Song:
    def __init__(self, title=None, artist=None, album=None, release_date=None, track_number=None, lyrics=''):
        self.title = title
        self.artist = artist
        self.release_date = release_date
        self.track_number = track_number
        self.lyrics = lyrics
        self.album = album
        
    def log_info(self, verbose=False):
        if verbose:
            print(f'Artist: {self.artist}',
                  f'\nAlbum: {self.album}',
                  f'\nTitle: {self.title}',
                  f'\nTrack: {self.track_number}',
                  f'\nRelease date: {self.release_date}')
        else:
            print(f'{self.artist} : {self.track_number:02d} {self.title}')