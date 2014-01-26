import platform

def return_darwin_linux(darwin, linux):
    os = platform.system()
    if os == "Darwin":
        return darwin
    elif os == "Linux":
        return linux
        
def getTestSampleDirectory():
    darwin = "/Users/smcho/temp/simulation"
    linux = "/home/smcho/temp/simulation"
    return return_darwin_linux(darwin, linux)
    
if __name__ == "__main__":
    print getTestSampleDirectory()