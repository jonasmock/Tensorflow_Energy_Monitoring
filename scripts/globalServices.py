class GlobalServices:

    import configparser

    __slots__ = ['pathToConfig']

    def __init__(self, **kwargs):

        print("This is the constructor method of \""+type(self).__name__+"\" class.")
        print("The following args are necessary: ", self.__slots__,"")

        for key, value in kwargs.items():
            try:
                setattr(self, key, value)
                pass
            except Exception as e:
                print("Can't init object.\n")
                raise Exception(e)

        print("Successfully initialized\n")

        pass


    # Reads config and returns value of a key in a specific section
    def readConfig(self, configSection, configKey):
        
        try:

            config = self.configparser.RawConfigParser()
            config.optionxform = str 
            config.read(getattr(self,"pathToConfig"))

            pass

        except Exception as e:

            print("Can't parse config.")
            print(e)
            print("\n")

            pass

        return config.get(configSection, configKey)


    # Reads config and returns it as dict
    def configToDict(self):
        
        try:

            config = self.configparser.RawConfigParser()
            config.optionxform = str 
            config.read(getattr(self,"pathToConfig"))

            pass

        except Exception as e:

            print("Can't parse config.")
            print(e)
            print("\n")

            pass

        return config._sections


    # Write value for specific key in a section to config file
    def writeConfig(self, configSection, configKey, keyValue):

        try:
            
            cfgfile = open(getattr(self,"pathToConfig"),'w')
            config = self.configparser.RawConfigParser()
            config.optionxform = str 
            config.read(getattr(self,"pathToConfig"))

            config.set(configSection, configKey, keyValue)
            config.write(cfgfile)
            cfgfile.close()

            pass

        except Exception as e:

            print("Can't write to config.")
            print(e)
            print("\n")

            pass

        pass
    

    pass

