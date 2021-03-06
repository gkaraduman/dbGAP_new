import os
import DatabaseOperations as wd
import FileProcessorThread as frt
from time import sleep

class dbGAPFileProcessor:
    def __init__(self, root_directory_path):
        self.root_directory_path = root_directory_path
        self.writeToDatabase = wd.DatabaseOperations()
        self.threads = []

    def __del__(self):
        for t in self.threads:
            t.join()
        print("Exiting Main Thread")

    def kill_finished_threads(self):
        self.threads = [t for t in self.threads if not t.done]

    def processDirectories(self):
        directory_list = list()

        for root, dirs, files in os.walk(self.root_directory_path, topdown=True):
            for name in dirs:
                directory_list.append(os.path.join(root, name))
            break

        for directory_path in directory_list:
            path_to_traverse = directory_path + "/analyses"
            if os.path.exists(path_to_traverse):
                for root, dirs, files in os.walk(path_to_traverse, topdown=True):
                    for name in files:
                        if (name != '.DS_Store' and name.startswith('._') == False):
                            self.study_id = name
                            while(len(self.threads) >= 10):
                                sleep(1)
                                self.kill_finished_threads()
                            try:
                                thread = frt.FileProcessorThread(path_to_traverse + "/" + name, self.writeToDatabase,
                                                                 self.study_id)
                                thread.start()
                                self.threads.append(thread)
                            except Exception as e:
                                print("Error: " + str(e))