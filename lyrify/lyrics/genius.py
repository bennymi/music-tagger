
from bs4 import BeautifulSoup
from pathlib import Path
import re
import requests

from lyrify.music.album import Album
from lyrify.music.song import Song
from lyrify.utils.errors import SongOrderValueError
from lyrify.utils.functions import log_function, log_sub_function


class GeniusLyrics:
    def __init__(self, lyrics_url, artist=None, album_title=None, folder_path=None, song_order=None, cover_size='600'):
        """
        Used to get the lyrics of a Genius lyrics page.
        
        Inputs:
            - album_url: URL to the Genius page of an album
            - single_url: URL to the lyrics of a single song
            - folder_path: path to the folder in which the cover art should be saved
        """
        self.album = Album(title=album_title, artist=artist)
        self.artist = artist
        self.album_title = album_title
        self.lyrics_url = lyrics_url
        self.song_order = song_order
        self.folder_path = Path(folder_path) if folder_path else None
        self.cover_file_name = 'cover.jpg'
        self.cover_size = f'{cover_size}x{cover_size}'
        self.track_urls = []
        self.cover_downloaded = False
        
        # self.r = requests.get(lyrics_url).text
        # self.soup = BeautifulSoup(self.r, 'html.parser')
        self.r = requests.get(lyrics_url)
        self.soup = BeautifulSoup(self.r.content, 'html.parser')
            
    def is_album(self):
        track_list = self.soup.findAll('div', class_='chart_row')
        if len(track_list) > 0:
            return True
        return False
    
    def create_folder(self, path=None, folder=None):
        self.folder_path = path / folder
        Path(self.folder_path).mkdir(parents=False, exist_ok=True)
    
    @log_function('Getting the information', ' ', show_time=True)
    def get_info(self, download_cover=True):
        if self.is_album():
            self.get_all_album_info(download_cover=download_cover)
        else:
            self.get_all_single_info(download_cover=download_cover)
        
        return self.album
        
    def get_all_album_info(self, download_cover=False):
        if self.folder_path and download_cover:
            self.cover_downloaded = self.download_album_cover()
            
        self.get_album_release_date()
        self.album.artist = self.artist if self.artist else self.get_album_artist()
        self.album.title = self.album_title if self.album_title else self.get_album_title()
        self.get_album_tracks()
        self.album.set_songs_release_date()
        self.album.set_songs_artist()       
    
    def get_all_single_info(self, url=None, download_cover=False):  
        if self.folder_path and download_cover:
            self.cover_downloaded = self.download_single_cover()
            
        title = self.get_single_title()
        artist = self.album.artist if self.album.artist else self.get_single_artist()
        album = self.album.title if self.album.title else self.get_single_album()
        release_date = self.album.release_date if self.album.release_date else self.get_single_release_date()
        lyrics = self.get_single_lyrics(url) if url else self.get_single_lyrics(self.lyrics_url)
        track_number = self.get_single_track_number()
        
        self.album.artist = artist
        self.album.release_date = release_date
        self.album.title = album
        self.album.add_song(Song(title, artist, album, release_date, track_number, lyrics))
    
    def get_single_artist(self):
        divs = self.soup.findAll('div')
        header = [x for x in divs if x.has_attr('class') and ('SongHeader__Column' in x['class'][0])]
        artist = None
        
        if len(header) > 0:
            artist = header[1].a.text.strip()
        else:
            for div in divs:
                if div.has_attr('class'):
                    if 'header_with_cover_art-primary_info' in div['class'][0] and div.h2 is not None:
                        artist = div.h2.text.strip()
                        break

        return artist
    
    def get_single_title(self):
        title = self.soup.find('h1').text.strip()
        return title
    
    def get_single_track_number(self):
        divs = self.soup.findAll('div')
        header = [x for x in divs if x.has_attr('class') and ('HeaderTracklist__AlbumLabel' in x['class'][0] or (len(x['class']) > 1 and 'track_listing-track--current' in x['class'][1]))]
        
        if len(header) > 0:
            track_re = re.compile('\d+')
            track = track_re.findall(header[0].text)
            if len(track) > 1:
                return int(track[0])
            else:
                return 1
        else:
            return 1
        
    def get_single_album(self):
        divs = self.soup.findAll('div')
        header = [x for x in divs if x.has_attr('class') and ('HeaderTracklist__Album-' in x['class'][0] or 'song_album-info' in x['class'][0])]
        
        if len(header) > 0:
            if header[0].a is not None:
                album = header[0].a.text.strip()
            else:
                album = header[0].text.strip()
            
            return album
        else:
            return None
    
    def get_single_release_date(self):
        date_re = re.compile('[a-zA-Z]+ \d+, \d{4}')
        release_date = None
        
        divs = self.soup.findAll('div')
        header = [x for x in divs if x.has_attr('class') and ('HeaderMetadata__Section-sc' in x['class'][0])]
        
        if len(header) == 0:
            spans = self.soup.findAll('span')
            header = [x for x in divs if x.has_attr('class') and ('metadata_unit' in x['class'])]
        
        if len(header) > 0:
            for head in header:
                dates = date_re.findall(head.text)
                if len(dates) > 0:
                    release_date = dates[0].replace('Date', '').strip()
        
        return release_date
    
    @log_sub_function('Downloaded song cover', 'Couldn\'t grab song cover')
    def download_single_cover(self):
        cover_downloaded = False
        if self.folder_path is None:
            raise ValueError('Folder path is not specified')
        
        try:
            all_divs = self.soup.findAll('div')
            filtered_divs = [x for x in all_divs if x.has_attr('class') and (('coverart' in x['class'][0].lower()) or ('cover_art' in x['class'][0].lower()))]
            
            single_cover_url = filtered_divs[0].find('img')['src']
        except Exception as e:
            single_cover_url = None
            print('Exception', e)
        
        if single_cover_url is not None:
            single_cover_url = re.sub(r'/[0-9]+x[0-9]+/', f'/{self.cover_size}/', single_cover_url)
            
            with open(self.folder_path / self.cover_file_name, 'wb') as f:
                f.write(requests.get(single_cover_url).content)
                self.cover_path = self.folder_path / self.cover_file_name
                cover_downloaded = True
        return cover_downloaded
    
    @log_sub_function('Downloaded album cover', 'Couldn\'t grab album cover')
    def download_album_cover(self):
        cover_downloaded = False
        if self.folder_path is None:
            raise ValueError('Folder path is not specified')
        
        try:
            album_cover_url = self.soup.find('img', class_='cover_art-image')['src']
        except Exception as e:
            album_cover_url = None
            print(e)
        
        if album_cover_url is not None:
            # We want a fixed album size: 600x600
            album_cover_url = re.sub(r'/[0-9]+x[0-9]+/', f'/{self.cover_size}/', album_cover_url)
            
            cover_path = self.folder_path / self.cover_file_name

            with open(cover_path, 'wb') as f:
                f.write(requests.get(album_cover_url).content)
                self.cover_path = cover_path
                cover_downloaded = True
        return cover_downloaded
    
    def get_album_title(self):
        title = self.soup.find('h1').text.strip()
        return title
    
    def get_album_artist(self):
        artist = self.soup.find('h2').text.strip()
        return artist
               
    def get_album_tracks(self):
        """
        Gets all the songs, along with their track number and the url to their lyrics
        from an album page.
        """
        track_list = self.soup.findAll('div', class_='chart_row')
        number_of_tracks = 0
        titles = []
        urls = []
        track_numbers = []
        
        for track in track_list:
            track_title = re.sub(' Lyrics', '', " ".join(track.h3.text.split()))
            lyrics_url = track.a['href']
            track_number = track.span.span.text.strip()
            
            if track_number == '':
                # Sometimes there are additional urls that are not a song's lyrics. Skip these.
                continue
            else:
                track_number = int(track_number)
            
            number_of_tracks += 1
            titles.append(track_title)
            urls.append(lyrics_url)
            track_numbers.append(track_number)
            
        if self.song_order:
            # Check that order values are okay.
            for number in self.song_order:
                if number > number_of_tracks:
                    raise SongOrderValueError(f'Track number given ({number}) exceeds number of tracks ({number_of_tracks})')
        
        for title, url, number in zip(titles, urls, track_numbers):
            if self.song_order:
                if number not in self.song_order:
                    print(f'Skipping song: {number:02d} {title}')
                    continue
            
            lyrics = self.get_single_lyrics(url)
            self.album.add_song(Song(title=title, track_number=number, lyrics=lyrics))

        self.album.number_of_tracks = number_of_tracks
            
    def get_album_release_date(self):
        header = self.soup.find('div', class_='header_with_cover_art-primary_info')
        search_release = re.compile(r'Released [a-zA-Z0-9,\s]+')
        release = search_release.findall(header.text)
        
        if len(release) > 0:
            self.album.release_date = re.sub('Released ', '', " ".join(release[-1].split()))
            
    def get_single_lyrics(self, url):
        """
        Lyrics on Genius usually are in multiple divs, all of which have a class of Lyrics__Container-sc-????? 
        with some random values, or they are inside a single div with a class of 'lyrics'.
        This function gets the lyrics and returns it.
        """
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        lyrics = ''
        
        all_divs = soup.findAll('div')
        filtered_divs = [x for x in all_divs if x.has_attr('class') and ('Lyrics__Container-sc' in x['class'][0] or x['class'] == ['lyrics'])]
        filtered_divs_classes = [x['class'] for x in filtered_divs if x.has_attr('class')]
        
        if len(filtered_divs) == 0:
            lyrics = ''
        elif len(filtered_divs) == 1 and filtered_divs_classes[0][0] == 'lyrics':
            lyrics = filtered_divs[0].text
        else:
            for part in filtered_divs:
                for e in part.descendants:
                    if isinstance(e, str):
                        lyrics += e.strip()
                    elif e.name == 'br' or e.name == 'p':
                        lyrics += '\n'
        
        return lyrics
    
    def get_all_lyrics(self):
        """
        This function is deprecated.
        """
        if len(self.track_urls) == 0:
            raise ValueError('URLs have not be retrieved yet. Call get_track_list() first.')
        
        if len(self.track_urls) == 0:
            return

        for url in self.track_urls:
            lyrics = self.get_single_lyrics(url)
            self.lyrics.append(lyrics)
