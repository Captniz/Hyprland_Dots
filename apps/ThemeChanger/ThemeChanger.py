########## SETUP ##########

import json
import yaml
import os
from rofi import Rofi
import subprocess
from shutil import copy

class themeReplacer: 
    """
    A class that replaces keywords in files with new values.

    Attributes:
    data (dict): A dictionary containing the configuration data for the replacements.

    Methods:
    SubsYaml(path, confile, category): Replaces keywords in a YAML file with new values.
    SubsJson(path, confile, category): Replaces keywords in a JSON file with new values.
    SubsText(path, confile, category): Replaces keywords in a text file with new values.
    SubsCommand(category): Runs a command specified in the configuration data.
    FileBackup(category): Creates a backup of the file being modified.
    substitutor(category): Determines the type of file being modified and calls the appropriate method to replace keywords.
    clearFile(path, confile): Clears the contents of a file and returns the original contents.
    """
    def __init__(self, data):
        """
        Initializes the themeReplacer object.

        Args:
        data (dict): A dictionary containing the configuration data for the replacements.
        """
        self.data = data
    
    def SubsYaml(self, path, confile, category):
        """
        Replaces keywords in a YAML file with new values.

        Args:
        path (str): The path to the file being modified.
        confile (str): The name of the file being modified.
        category (str): The category of the configuration data being used.

        Returns:
        None
        """
        with open(path + confile, 'r') as f:
            filedata = yaml.safe_load(f)
            for keyword in self.data[category]["configs"]:
                filedata[keyword] = self.data[category]["configs"][keyword]
        with open(path + confile, 'w') as f:
            yaml.dump(filedata,f)
        return    
    
    def SubsJson(self, path, confile, category):
        """
        Replaces keywords in a JSON file with new values.

        Args:
        path (str): The path to the file being modified.
        confile (str): The name of the file being modified.
        category (str): The category of the configuration data being used.

        Returns:
        None
        """
        with open(path + confile, 'r') as f:
            filedata = json.load(f)
            for keyword in self.data[category]["configs"]:
                filedata[keyword] = self.data[category]["configs"][keyword]
        with open(path + confile, 'w') as f:
            json.dump(filedata,f,indent=4)

    def SubsText(self, path, confile, category):
        """
        Replaces keywords in a text file with new values.

        Args:
        path (str): The path to the file being modified.
        confile (str): The name of the file being modified.
        category (str): The category of the configuration data being used.

        Returns:
        None
        """
        file = self.clearFile(path,confile)
        with open(path + confile, 'w') as f:
            for line in file.splitlines():
                def TextSubstitutor(data,line,file,category):
                    for word in line.split():
                        for keyword in data[category]["configs"]:
                            if keyword == word:
                                file.write(data[category]["configs"][word]+"\n")
                                return 
                    file.write(line+"\n")
                    return 
                TextSubstitutor(self.data,line,f,category)

    def SubsCommand(self, category):
        """
        Runs a command specified in the configuration data.

        Args:
        category (str): The category of the configuration data being used.

        Returns:
        None
        """
        for command in self.data[category]["configs"]:
            subprocess.run(command, shell=True)

    def FileBackup(self, category):
        """
        Creates a backup of the file being modified.

        Args:
        category (str): The category of the configuration data being used.

        Returns:
        tuple: A tuple containing the path and name of the file being modified.
        """
        path = self.data[category]["path"]
        confile = self.data[category]["confile"]
        if path == "" or confile == "":
            return
        copy(path + confile, path + "older-" +confile)
        return (path, confile)

    def substitutor(self, category):
        """
        Determines the type of file being modified and calls the appropriate method to replace keywords.

        Args:
        category (str): The category of the configuration data being used.

        Returns:
        None
        """
        fileData = self.FileBackup(category)

        def switch(type):
            if type == "yaml":
                self.SubsYaml(fileData[0],fileData[1],category);
            elif type == "json":
                self.SubsJson(fileData[0],fileData[1],category);
            elif type == "text":
                self.SubsText(fileData[0],fileData[1],category);
            elif type == "command":
                self.SubsCommand(category);
            else:
                print("Error: type not supported")
            return
        switch(self.data[category]["type"])

    def clearFile(self, path, confile):
        """
        Clears the contents of a file and returns the original contents.

        Args:
        path (str): The path to the file being modified.
        confile (str): The name of the file being modified.

        Returns:
        str: The original contents of the file.
        """
        with open(path + confile, 'r+') as f:
            f.seek(0)
            file = f.read()
            f.truncate(0)
            f.seek(0)
        return file

def getFileNames():
    """
    Get the names of all the possible themes to change.

    Returns:
    list: Name of the themes.
    """
    return os.listdir(f"{os.path.dirname(__file__)}/Themes")

########## MAIN ##########
def main():

    # Input theme
    themes = getFileNames();
    r = Rofi();
    index, key = r.select("Choose a theme", themes)


    # Load theme data
    with open(f"{os.path.dirname(__file__)}/Themes/{themes[index]}", 'r') as f:
        data = json.load(f)

    # Apply theme
    for cat in data:
        if cat != "firefox": #Test single configs
            themeReplacer(data).substitutor(cat)

    return

if __name__ == "__main__":
    main()


#TODO:
    # - aggiugni dunst
    # - fix firefox: guarda in prefs.js in alto il commento
    # - fix firefox: user js cambia anche theme.toolbar 1=light 0=dark
    # - fix firefox
    # - restore "older-files"
    # - auto detect text/json/yaml
    # - Il theme changer di rofi sarebbe meglio se agisse su il tema nel config di rofi al posto di cambiare solo i colori
    # - metti su rofi

    # PROTOTYPE FIREFOX THEME CHANGER
    '''
            path = data["firefox"]["path"]
            confile = data["firefox"]["confile"]
            copy(path + confile, path + "older-" +confile)
            
            with open(path + confile, 'r') as f:
                filedata = json.load(f)
            for keyword in filedata["addons"]:
                if keyword["type"] == "theme":
                    if keyword["active"] == True:
                        keyword["active"] = False
                        keyword["userDisabled"] = True
                    if keyword["defaultLocale"]["name"] == data["firefox"]["configs"]["theme"]:
                        keyword["active"] = True
                        keyword["userDisabled"] = False
            with open(path + confile, 'w') as f:
                json.dump(filedata,f,indent=4)
            
            with open(path + confile, 'r+') as f:
                f.seek(0)
                file = f.read()
                f.truncate(0)
                f.seek(0)
            with open(path + confile, 'w') as f:
                for line in file.splitlines():
                    def TextSubstitutor(line,file,category):
                        for word in line.split():
                            if word == "user_pref(\"extensions.activeThemeID\",":
                                file.write(cdata[category]["configs"]["user_pref(\"extensions.activeThemeID\","] +"\n")
                            return 
                        file.write(line+"\n")
                        return 
                    TextSubstitutor(line,f,cat) #TODO: FIXXALL
            '''