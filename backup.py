import os
import shutil
import logging 
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logging.basicConfig(
    filename="logs/backup.log",
    level=logging.INFO,
    format="%(asctime)s -%(message)s"
)
source_dir = "source_files"
backup_dir = "backup_files"

class backupHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        
        filename = os.path.basename(event.src_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        backup_file = os.path.join(backup_dir, f"backup_{timestamp}_{filename}")

        
        shutil.copytree(
            source_dir,
            backup_file
        )

        logging.info(
            f"Backup succesful: {backup_file}"
        )
        print("Backup completed")
    
        backup_folders = sorted(os.listdir(backup_dir))
        if len(backup_folders) > 5:
            old_backups = backup_folders[:-5]

            for folder in old_backups:
                shutil.rmtree(
                    os.path.join(
                    backup_dir,
                    folder
                    )
                )
            logging.info(f"old folder deleted succefully: {folder}")

event_handler = backupHandler()
observer = Observer()



observer.schedule(
        event_handler,
        source_dir,
        recursive=False
    )

observer.start()

print("watching for changes....")

try:
        while True:
            pass
except KeyboardInterrupt:
        observer.stop()

observer.join()


    
