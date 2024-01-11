import shutil as sh
import sys
import os
import json

# TODO Tee help tiedosto ja komento mikä printtaa sen komentoriville.
# TODO Tee komento, millä voi lisätä kurssi, arkistokansio parin asetuksiin.
# TODO Lisää asetuksiin muita yliopistoja/kaikki kurssit jyulta.
# TODO Tee metodi jolla voidaan siirtää tiedosto/kansio arkistorakenteen tiettyyn kansioon
class Archive:

    # Constructor
    def __init__(self):
        self.working_directory = os.getcwd()
        self.settings = self.read_json_file("settings.json")
        self.archive_path = self.settings["path"]
        self.university = self.settings["uni"]



    # Returns source address for file/folder
    def get_source_address(self, folder):
        return self.working_directory + "\\" + folder


    def file_address(self, file_name):
        return file_name.split('.')[0].split('_')[0]


    # Returns destination address for each file. If folders don't exist, they are created.
    def get_destination_address(self, folder):
        base = self.archive_path
        foldernames = self.settings.get(self.university,{}).get("foldernames", [])
        specification = self.settings.get(self.university,{}).get("courselevel", [])
        corresponding = self.settings.get(self.university,{}).get("coursebeginning", [])

        for member, foldername in zip(corresponding, foldernames):    
            if folder[:3].lower() == member:
                base = base + foldername        
                for member in specification:
                
                    if folder[3].lower() == member[0].lower():
                        base = base + "\\" + member
                        break
                break
        if base == self.archive_path: # If file doesnt match any course it still archives.
            base = base + "\\unsorted"

        if os.path.isfile(self.working_directory + '\\' + folder): # If there is files, they will be moved to correct folder. Naming course_assignment.end.
            base = base + '\\' + self.file_address(folder)

        os.makedirs(base, exist_ok=True) # Makes directory if it doesn't exist.
        return base


    # Performs a single transfer.
    def move(self, source, destination):
        try:
            sh.move(source, destination)
            print("Transfer successfully completed")
        except:
            print("Incorrect source or destination path.")
   

    # Transfers the files given as a parameter.
    def no_paramerters(self, files):
        for file in files:            
            self.move(self.get_source_address(file), self.get_destination_address(file))

            
    # Moves everything from the working directory to the archive.
    def moveall(self):
        files = os.listdir()
        self.no_paramerters(files)


    # Transfers everything except the files given as a parameter.
    def moveall_except(self, files_exc):
        files = os.listdir()
        for file in files_exc:
            files.remove(file)
    
        self.no_paramerters(files)


    # Changes script settings
    def change_settings(self, setting, new_value):
        self.settings[setting] = new_value
        self.write_json_file("settings.json", self.settings)

    # Prints instructions
    def print_help(self):
        print(self.read_file("instructions.txt"))


    # Reads .json file
    @staticmethod
    def read_json_file(name):
        # for some reason this is needed whenever files are accessed.
        script_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(script_dir, name)
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    

    # Writes .json file
    @staticmethod
    def write_json_file(name, data):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(script_dir, name)
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    # Reads normal .txt file.
    @staticmethod
    def read_file(name):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(script_dir, name)
        with open(file_path, 'r') as file:
            data = file.read()
        return data


# Main program
def main():
    a = Archive()

    # Checks if some command is given as parameter.
    try:
        if sys.argv[1][0] == '-':
            files = sys.argv[2:]
            if sys.argv[1] == "-a":
                a.moveall() 
            if sys.argv[1] == "-e":
                a.moveall_except(files)
            if sys.argv[1] == "-p" or sys.argv[1] == "-path":
                a.change_settings("path", sys.argv[2])
            if sys.argv[1] == "-u" or sys.argv[1] == "-university":
                a.change_settings("uni", sys.argv[2])
            if sys.argv[1] == "-h" or sys.argv[1] == "-help":
                a.print_help()  
        else:       
            files = sys.argv[1:]
            a.no_paramerters(files)
    except Exception as e:
        print("No parameters given. " + e)
       

if __name__ == "__main__":

    main()