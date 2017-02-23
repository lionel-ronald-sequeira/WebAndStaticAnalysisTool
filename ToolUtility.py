import subprocess,os;
from DBOperation import DBOperation;
def flawFinder(userfolderpath,userfilepath,fileName,username,dbObj):
    try:
        print "Start flawfinder";
        resultfilename=fileName.rsplit('.',1)[0];
        print "ResultFileName "+resultfilename;
        resultfile="flawfinder"+"-"+resultfilename+".txt";
        resultfilepath=userfolderpath+"/"+resultfile;
        print "ResultFilePath",resultfilepath;
        #subprocess.Popen('flawfinder ' + userfilepath + " > " + resultfilepath, shell=True);
        ps=subprocess.Popen('flawfinder '+userfilepath+" > "+resultfilepath, shell=True);
        ps.communicate()
        dbObj.storeToolResult(fileName, username, '', 'flawfinder',resultfile);
        if os.path.exists(resultfilepath):
            f = open(resultfilepath, 'r')
            flawfinderResult = f.read();
            f.close();
            dbObj.updateToolResult(fileName, resultfile, username, flawfinderResult);
            print "Flawfinder result :";
            print flawfinderResult;
            subprocess.Popen('rm '+resultfilepath, shell=True);
        print "End flawfinder";
    except Exception as e:
        print "Exception : flawFinder";
        raise e;



def rats(userfolderpath,userfilepath,fileName,username,dbObj):
    try:
        print "Start rats";
        resultfilename=fileName.rsplit('.',1)[0];
        print "ResultFileName "+resultfilename;
        resultfile="rats"+"-"+resultfilename+".txt";
        resultfilepath=userfolderpath+"/"+resultfile;
        print "ResultFilePath",resultfilepath;
        #subprocess.Popen('rats --quiet --html -w 3 ' + userfilepath + " > " + resultfilepath, shell=True);
        ps=subprocess.Popen('rats --quiet -w 3 '+userfilepath+" > "+resultfilepath, shell=True);
        ps.communicate();
        dbObj.storeToolResult(fileName, username, '', 'rats',resultfile);
        if os.path.exists(resultfilepath):
            f = open(resultfilepath, 'r')
            ratsResult = f.read();
            f.close();
            dbObj.updateToolResult(fileName,resultfile,username,ratsResult);
            subprocess.Popen('rm '+resultfilepath, shell=True);
        print "End rats"
    except Exception as e:
        print "Exception : rats";
        raise e;