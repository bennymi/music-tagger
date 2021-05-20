
import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TALB, TPE1, TPE2, COMM, USLT, TCOM, TCON, TDRC, TRCK, TORY, TDOR, TYER, TDRL, TDAT
import re

from lyrify.utils.functions import convert_date, log_function
from lyrify.utils.errors import SongOrderLengthError, SongOrderValueError

class MusicTagger:
    def __init__(self, path, album, order=None):
        self.path = Path(path)
        self.album = album
        self.order = order
        self.cover_name = 'cover.jpg'
        
        self.song_paths = [(self.path / f) for f in listdir(self.path) if isfile(join(self.path, f)) and f.endswith('.mp3')]
        
        if order:
            # Check that order values are okay.
            if len(self.song_paths) != len(order):
                raise SongOrderLengthError(f'The number of songs given in songs_order ({len(order)}) does not match the number of music files ({len(self.song_paths)}) in the path: {path}')
            
            for number in order:
                if number > self.album.number_of_tracks:
                    raise SongOrderValueError(f'Track number given ({number}) exceeds number of tracks ({self.album.number_of_tracks})')
        
        self.songs = [album.songs[i - 1] for i in order] if order else self.album.songs
        
    
    @log_function('Tagging Songs', ' ', show_time=True)
    def tag_songs(self):
        for path, song in zip(self.song_paths, self.songs):
            cover_added = False
            lyrics_added = False
            
            tags = ID3()
            
            tags["TIT2"] = TIT2(encoding=3, text=song.title) # Title
            tags["TALB"] = TALB(encoding=3, text=self.album.title) # Album
            tags["TPE2"] = TPE2(encoding=3, text=self.album.artist) # Band/Orchestra/Accompaniment
            tags["TPE1"] = TPE1(encoding=3, text=self.album.artist) # Lead Artist/Performer/Soloist/Group
            tags["TRCK"] = TRCK(encoding=3, text=str(song.track_number)) # Track number
            tags["USLT"] = USLT(encoding=3, text=song.lyrics) # Lyrics
            
            if len(song.lyrics) > 0:
                lyrics_added = True
            
            if self.album.release_date:
                re_year = re.compile(r'\d{4}')
                year = re_year.findall(self.album.release_date)
                release_time = convert_date(self.album.release_date)
                
                if len(year) > 0 and len(year[0]) > 0:
                    year = year[0]
                    tags["TORY"] = TORY(encoding=3, text=year) # Original Release Year
                    tags["TDRC"] = TDRC(encoding=3, text=year) # Recording time
                    tags["TDOR"] = TDOR(encoding=3, text=year) # Official Release Time
                    tags["TYER"] = TYER(encoding=3, text=year) # Year of Recording
                    tags["TDRL"] = TDRL(encoding=3, text=release_time) # Release Time
            
            tags.save(path, v2_version=3)
            
            # audio = ID3(path)
            # print(f'{audio["TPE1"].text[0]} {audio["TDRC"].text[0]} {audio["TRCK"].text[0]} {audio["TIT2"].text[0]}')
            
            cover_path = str(self.path / self.cover_name)
            
            if os.path.isfile(cover_path):
                audio = MP3(path, ID3=ID3)
                audio.tags.add(APIC(mime='image/jpeg', type=3, desc=u'Cover', data=open(str(cover_path),'rb').read()))
                audio.save(v2_version=3)
                cover_added = True
            
            self.log_information(path, self.album.artist, self.album.title, song.title, song.track_number, year, cover_added, lyrics_added)
        
    def log_information(self, path, artist, album, title, track, year, cover_added=False, lyrics_added=False):
        lyrics = "Lyrics Added" if lyrics_added else "No Lyrics"
        cover = "Cover Added" if cover_added else "No Cover"
        log = f"{lyrics:12} | {cover:11} | Artist: {artist} | Album: {album} | Release: {year} | Track: {track:02d} {title}" 
        print(log)