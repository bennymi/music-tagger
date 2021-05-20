import argparse

from lyrify.utils.functions import parse_order

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder_path", type=str, required=True, help="Path to the parent folder in which the new album folder should be saved")
    parser.add_argument("--album_title", type=str, required=False, default=None, help="Specify the name of the album that shold be used. If no name is specified, the album name will be used that is found on the lyrics page.")
    parser.add_argument("--artist", type=str, required=False, default=None, help="Specify the name of the artist that shold be used. If no name is specified, the artist name will be used that is found on the lyrics page.")
    parser.add_argument("--lyrics_url", type=str, required=True, default=None, help="URL to the album or singles page on genius.com")
    # parser.add_argument("--type", type=str, required=False, default="album", choices=['album', 'single'], help='Type of Genius page: an abum page or a page to a single song\'s lyrics')
    parser.add_argument('--song_order', nargs='+', required=False, help='Order in which the songs in the folder are using the track numbers from the lyrics page. Leave out track numbers if some songs are missing in the folder that are on the lyrics page.')
    parser.add_argument('--cover_size', type=int, required=False, default=600, help='The size the downloaded cover should be. Eg. entering 500 leads to a cover size of 500x500. The default size is 600x600.')
    args = parser.parse_args()
    
    if args.song_order:
        # Convert the list of strings in song order to a list of integers
        args.song_order = parse_order(args.song_order)
    
    return args