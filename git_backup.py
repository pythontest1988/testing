import os
import time
import shutil
import logging
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

repo_path = r"D:\automation project"

logging.basicConfig(
    filename="logs/git_backup.log",
    level=logging.INFO,
    force="%(asctime)s -%(message)s"

)

class Githandler(FileSystemEventHandler):

    def push_to_github(self):
        try:
            subprocess.run(
                ["git", "add", "."],
                cwd= repo_path,
                check=True
            )

            #logging.INFO(f"git status added sucessfully")

            subprocess.run(
                ["git", "commit", "-m", "Auto backup"],
                cwd=repo_path,
                check=True
            )

            #logging.INFO(f"git commited successfully")

            subprocess.run(
                ["git", "push"],
                cwd=repo_path,
                check=True
            )

            #logging.INFO(f"changes pushed successfully")

            print("Changes pushed to git repo")

        except subprocess.CalledProcessError as e:
            print(f"git error: {e}")
        
    def on_created(self, event):
        if not event.is_directory:
            print(f"created: {event.src_path}")
            self.push_to_github()

    def on_modified(self, event):
        if not event.is_directory:
            print(f"modified: {event.src_path}")
            self.push_to_github()

event_handler = Githandler()

observer = Observer()
observer.schedule(event_handler, repo_path, recursive=True)

observer.start()

print("wating for changes")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()


observer.join()

        