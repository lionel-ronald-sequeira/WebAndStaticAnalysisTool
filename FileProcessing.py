import subprocess,os
#import magic
import ToolUtility
import glob
from DBOperation import DBOperation;

def uploadFileToFolder(file,uploadfolderpath,username,filename,dbObj):
    try :
        print "Start uploadFileToFolder";
        userfolderpath = uploadfolderpath + "/" + username;
        print "User folder path :", userfolderpath;
        if not os.path.isfile(userfolderpath):
            ps = subprocess.Popen('mkdir ' + userfolderpath, shell=True);
            ps.communicate();
        userfilepath = userfolderpath + "/" + filename;
        print "User file path :", userfilepath;
        mimetype = getMimeTypeForFile(file);
        file.save(os.path.join(userfolderpath, filename));
        print mimetype;
        selectToolForProcessing(mimetype, userfolderpath, userfilepath, filename, username,dbObj);
        # ToolUtility.flawFinder(userfolderpath,userfilepath,filename,username);
        deleteFile(os.path.join(userfolderpath, filename));
        print "End uploadFileToFolder";
    except Exception as e:
        print "Exception : uploadFileToFolder";
        deleteFile(os.path.join(userfolderpath, filename));
        raise e;


def selectToolForProcessing(mimetype,userfolderpath, userfilepath, filename, username,dbObj):
    try :
        print "Start selectToolForProcessing";
        if mimetype == 'text/x-python' or mimetype == 'text/x-php' or mimetype == 'text/x-perl':
            ToolUtility.rats(userfolderpath, userfilepath, filename, username);
        elif mimetype == 'text/x-c':
            print "MimeType text/x-c";
            ToolUtility.flawFinder(userfolderpath, userfilepath, filename, username,dbObj);
            ToolUtility.rats(userfolderpath, userfilepath, filename, username,dbObj);
        print "End selectToolForProcessing";
    except Exception as e:
        print "Exception : selectToolForProcessing";
        raise e;


def getMimeTypeForFile(file):
    try :
        print "Start getMimeTypeForFile";
        mimetype ='';# magic.from_buffer(file.read(1024), mime=True);
        file.seek(0);
        print "End getMimeTypeForFile";
        return mimetype;
    except Exception as e:
        print "Exception : getMimeTypeForFile";
        raise e;

def getToolResults(username,folderpath):
    try :
        print "Start getToolResults";
        userfolderpath = folderpath + "/" + username;
        files=glob.glob(userfolderpath+"/*.txt");
        dbObj=DBOperation();
        dbObj.openConnectionToDB();
        for file in files:
            print "Filename :",file;
            if "flawfinder" in file or "rats" in file:
                f = open(file, 'r')
                toolResult = f.read();
                f.close();
                resultfileName=file.rsplit("/",1)[1];
                print resultfileName;
                dbObj.updateToolResult(None, resultfileName, username, toolResult);
                deleteFile(file);
        resultList=dbObj.getToolResult(username);
        dbObj.closeConnectionToDb();
        return resultList;
        print "End getToolResults";
    except Exception as e:
        print "Exception : getToolResults";
        raise e;


def deleteFile(filePath):
    try :
        subprocess.Popen('rm ' + filePath, shell=True);
    except Exception as e:
        print "Exception : deleteFile";
        raise e;




