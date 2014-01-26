import platform
import os.path

def return_darwin_linux(darwin, linux):
    s = platform.system()

    if s == "Darwin":
        assert os.path.exists(darwin), "Directory missing %s" % linux
        return darwin
    elif s == "Linux":
        assert os.path.exists(linux), "Directory missing %s" % linux
        return linux

def getTestSimpleDirectory():
    darwin = "./test/testFile"
    linux = darwin
    return return_darwin_linux(darwin, linux)  
        
def getTestDirectory():
    darwin = "/Users/smcho/temp/simulation"
    linux = "/home/smcho/temp/simulation"
    return return_darwin_linux(darwin, linux)
    
def getSampleFile():
    darwin = "./test/testFile/sample.txt"
    return return_darwin_linux(darwin, darwin)
    
if __name__ == "__main__":
    print getTestSimpleDirectory()
    print getTestDirectory()
    print getSampleFile()