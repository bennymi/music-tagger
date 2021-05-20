# Lyrify : music-tagger
__Lyrify__ is a simple CLI program to add lyrics as well as other information from genius.com to your music. For now only .mp3 files are supported.

Install with:

```console
pip install lyrify
```

To add lyrics to an album simply run **sing** with the **--folder_path** and **--lyrics_url** options. This also works with single songs, so if you use a direct link to a song's lyrics.

**Album:**
```console
lyrify --folder_path "C:\Users\User\Music\BTS\BTS - BE" --lyrics_url https://genius.com/albums/Bts/Be
```

**Single:**
```console
lyrify --folder_path "C:\Users\User\Music\Ed Sheeran\Afterglow" --lyrics_url https://genius.com/Ed-sheeran-afterglow-lyrics
```

If there are more songs on the album page than you have in your folder or if the order of the songs in your folder are not the same as in the album page, you have to use the **--song_order** flag to specify which tracks and in which order they are. Additional options include:

```console
--artist        Adds the ARIST name to the mp3 files instead of 
                using the name found on the genius.com page.

--album_title   Adds the ALBUM_TITLE to the mp3 files instead 
                of using the album title found on the genius.com page.

--cover_size    An integer value specifying the size the downloaded 
                album/song cover should be (the default is 600 -> 600x600).

--song_order    The order of the songs as they are found in your folder_path. 
                If you are missing some songs, simply leave them out. Separate 
                track numbers by spaces or commas. Ranges are accepted (5-8).
```

Example of using **--song_order** if you only have songs 1, 2, 5, 6, 7, 8 of an album: 

```console
lyrify --folder_path "C:\Users\User\Music\Ed Sheeran\Divide" --lyrics_url https://genius.com/albums/Ed-sheeran/Divide --song_order 1, 2, 5-8
```

To use it in **Python**:

```python
from lyrify.lyrics.genius import GeniusLyrics
from lyrify.music.music_tagger import MusicTagger

...

gl = GeniusLyrics(lyrics_url=lyrics_url, artist=artist, album_title=album, folder_path=folder, song_order=song_order, cover_size=cover_size)
gl.get_info()

mt = MusicTagger(folder_path, album=gl.album, order=song_order)
mt.tag_songs()
```

Check out the code on [GitHub](https://github.com/bennymi/music-tagger).