## File Management Script built to automatically sort and move downloaded files into corresponding folders on MacBook.

from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Destination Folder Paths
src_download_dir_path = "/Users/ryearwood/Downloads"
dest_dir_music = "/Users/ryearwood/Desktop/Downloaded Music"
dest_dir_video = "/Users/ryearwood/Desktop/Downloaded Videos"
dest_dir_pictures = "/Users/ryearwood/Desktop/Downloaded Pictures"
dest_dir_documents = "/Users/ryearwood/Desktop/Downloaded Documents"
dest_other_files = "/Users/ryearwood/Desktop/Downloaded Other Files"

# Supported File Type Extensions
music_filetypes_extensions = [".mp3", ".m4a", ".wav",".wma",".flac", ".aiff", ".alac", ".aac"]
video_filetypes_extensions = [".flv", ".webm", ".gif", ".avi", ".mov", ".qt", ".wmv", ".amv",".mp4"]
picture_filetypes_extensions = [".jpeg",".jpg",".svg",".png",".PNG", ".webp"]
document_filetypes_extensions = [".doc", ".docx", ".odt", ".pdf",".txt", ".xls", ".xlsx",".ppt", ".pptx"]

def update_existing_filename(dest_filepath: str, filename: str) -> str:
    """Updates the downloaded filename if file already exists at the the destination 
    folder path.

    Args:
        dest_filepath (str): Destination folder path for the downloaded file.
        filename (str): Name of file being moved.
    
    Returns: str: Modified filename if file already exists.
    """
    filename, extension = splitext(filename)
    counter = 1
    while exists(f"{dest_filepath}/{filename}"):
        updated_name = f"{filename}({str(counter)}){extension}"
        counter += 1
    return updated_name

def move_file(dest_filepath: str, file_path: str, filename: str) -> None:
    """Moves a file to the designated folder. Renames the file if it already exists.

    Args:
        dest_filepath (str): This is the designated folder path for the item to be moved to.
        file (str): This is the filepath of the item to be moved.
        filename (str): Name of the file to be moved.
    """
    file_exists = exists(dest_filepath + "/" + filename)
    if file_exists:
        updated_filename = update_existing_filename(dest_filepath, filename)
        old_name = join(dest_filepath, filename)
        new_name = join(dest_filepath, updated_filename)
        rename(old_name, new_name)
    move(file_path, dest_filepath)
    

class FileMoveHandler(FileSystemEventHandler):
    """Runs the subsequent file management functions whenever there is a change in the 
    'src_download_dir_path'.

    Args:
        FileSystemEventHandler(class): Watchdog event handler for monitoring changes in
            the specified directory.
    """
    def on_modified(self, event):
        logging.info("Downloader Folder Updated.... Automating File Management ")
        with scandir(src_download_dir_path) as downloaded_files:
            for each_file in downloaded_files:
                if not self.verify_filename(each_file.name):
                    continue
                if self.verify_move_image_files(each_file, each_file.name):
                    continue
                elif self.verify_move_audio_files(each_file, each_file.name):
                    continue
                elif self.verify_move_video_files(each_file, each_file.name):
                    continue
                elif self.verify_move_document_files(each_file, each_file.name):
                    continue
                else:
                    move_file(dest_other_files, each_file, each_file.name)
    
    def verify_filename(self, filename: str) -> bool:
        """Verifies the filename as True unless hidden file detected, then returns False.
        Hidden Files begin with '.'

        Args:
            filename (str): Retrieved Filename

        Returns:
            bool: True if valid filename. False if Hidden File.
        """
        if filename.startswith("."):
            return False
        return True
    
    def verify_move_image_files(self, filepath: str, filename: str) -> bool:
        """Verifies if downloaded file is an image type file and moves it to the designated
        folder.

        Args:
            filepath (str): Downloaded item's filepath
            filename (str): Filename of the downloaded image item
        
        Returns:
            bool: True if file moved successfully.
        """
        if splitext(filepath)[1].lower() in picture_filetypes_extensions:
            move_file(dest_dir_pictures, filepath, filename)
            logging.info(f"Moved Image File: {filename}")
            return True
        return False
        
    def verify_move_audio_files(self, filepath: str, filename: str) -> bool:
        """Verifies if downloaded file is an audio type file and moves it to the designated
        folder.

        Args:
            filepath (str): Downloaded item's filepath
            filename (str): Filename of the downloaded audio item.
            
        Returns:
            bool: True if file moved successfully.
        """
        if splitext(filepath)[1].lower()in music_filetypes_extensions:
            move_file(dest_dir_music, filepath, filename)
            logging.info(f"Moved Audio File: {filename}")
            return True
        return False
                
    def verify_move_video_files(self, filepath: str, filename: str) -> bool:
        """Verifies if downloaded file is a video type file and moves it to the designated
        folder.

        Args:
            filepath (str): Downloaded item's filepath
            filename (str): Filename of the downloaded video item.
        
        Returns:
            bool: True if file moved successfully.
        """
        if splitext(filepath)[1].lower() in video_filetypes_extensions:
            move_file(dest_dir_video, filepath, filename)
            logging.info(f"Moved Video File: {filename}")
            return True
        return False
    
    def verify_move_document_files(self, filepath: str, filename: str) -> bool:
        """Verifies if downloaded file is a document type file and moves it to the designated
        folder.

        Args:
            filepath (str): Downloaded item's filepath
            filename (str): Filename of the downloaded document item.
        
        Returns:
            bool: True if file moved successfully.
        """
        if splitext(filepath)[1].lower() in document_filetypes_extensions:
            move_file(dest_dir_documents, filepath, filename)
            logging.info(f"Moved Document File: {filename}")
            return True
        return False
        
if __name__ == "__main__":
    
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = src_download_dir_path
    event_handler = FileMoveHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    logging.info("Process Started")
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        logging.info("Terminating Process")
        observer.stop()
    observer.join()