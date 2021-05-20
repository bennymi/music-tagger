# Lyrify : music-tagger
__Lyrify__ is a simple CLI program to add lyrics as well as other information from genius.com to your music (.mp3) files.

To add lyrics to an album simply run **sing** with the **--folder_path** and **--lyrics_url** options:

```console
sing --folder_path "C:\Users\User\Music\BTS\BTS - BE" --lyrics_url https://genius.com/albums/Bts/Be
```

Additional options include:

```console
--artist    Adds the ARIST name to the mp3 files instead of 
            using the name found on the genius.com page.

--album_title   Adds the ALBUM_TITLE to the mp3 files instead 
                of using the album title found on the genius.com page.

--cover_size    An integer value describing the size the downloaded 
                album/song cover should be (the default is 600 -> 600x600).

--song_order    The order of the songs as they are found in your folder_path. 
                If you are missing some songs, simply leave them out. Separate 
                track numbers by spaces or commas. Ranges are accepted (5-8).
```

Example of using **--song_order** if you only have songs 1, 2, 5, 6, 7, 8 of an album: 

```console
sing --folder_path "C:\Users\User\Music\Ed Sheeran\Divide" --lyrics_url https://genius.com/albums/Ed-sheeran/Divide --song_order 1, 2, 5-8
```