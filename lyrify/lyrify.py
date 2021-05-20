from lyrify.lyrics.genius import GeniusLyrics
from lyrify.music.music_tagger import MusicTagger
from lyrify.utils.arguments import get_arguments
from lyrify.utils.functions import log_function

# TODO: Add the ability to post all links and file paths in a txt file
# the code then executes for each link and file path in the txt file

class Lyrify:
    def __init__(self, lyrics_url, folder, artist=None, album=None, song_order=None, cover_size=600):
        self.gl = GeniusLyrics(lyrics_url=lyrics_url, artist=artist, album_title=album, folder_path=folder, song_order=song_order, cover_size=cover_size)
        self.mt = None
        self.folder_path = folder
        self.song_order = song_order
    
    @log_function('', ' ', show_time=True, duration_msg='-> Total Duration')
    def add_lyrics(self):
        self.gl.get_info()
        self.gl.album.log_info()
        self.mt = MusicTagger(self.folder_path, album=self.gl.album, order=self.song_order)
        self.mt.tag_songs()

def lyrify_cli():
    args = get_arguments()
    
    l = Lyrify(args.lyrics_url, args.folder_path, args.artist, args.album_title, args.song_order, args.cover_size)
    l.add_lyrics()

if __name__ == '__main__':
    lyrify_cli()

# Examples:

# sing --folder_path "C:\Users\BennySoul\Documents\Coding\My Projects\album-downloader\images" --lyrics_url https://genius.com/albums/Ed-sheeran/Divide --album_title "Divide" --song_order 1, 2, 3, 4, 5

# sing --folder_path "C:\Users\BennySoul\Music\Korean Music (KPop)\OH MY GIRL\숲의 아이 (Bon Voyage)" --lyrics_url https://genius.com/albums/Yooa/Bon-voyage

# sing --lyrics_url https://genius.com/albums/K-da/All-out --folder_path "C:\Users\BennySoul\Music\Korean Music (KPop)\KDA\All Out" --artist KDA

# sing --lyrics_url https://genius.com/Ed-sheeran-shape-of-you-lyrics --folder_path "C:\Users\BennySoul\Music\Ed Sheeran\Shape Of You - Copy"