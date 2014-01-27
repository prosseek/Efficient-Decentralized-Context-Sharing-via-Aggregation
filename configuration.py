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
    else:
        raise Exception("Only Mac or Linux is supported")
        

def getTestSimpleDirectory():
    darwin = "./test/testFile"
    linux = darwin
    return return_darwin_linux(darwin, linux)  
        
def getTestDirectory():
    darwin = "/Users/smcho/temp/simulation"
    linux = "/home/smcho/temp/simulation"
    return return_darwin_linux(darwin, linux)
    
def getResultsDirectory():
    return os.path.join(getTestDirectory(), "results")
    
def getDataDirectory():
    return os.path.join(getTestDirectory(), "data")
    
def getSampleFile():
    darwin = "./test/testFile/sample.txt"
    return return_darwin_linux(darwin, darwin)
    
if __name__ == "__main__":
    print getTestSimpleDirectory()
    print getTestDirectory()
    print getSampleFile()
    print getResultsDirectory()
    print getDataDirectory()
    