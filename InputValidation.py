import re

def checkUsername(username):
    pattern = '^[A-Za-z0-9_]{6,15}$';
    flag = True;
    if re.match(pattern,username, flags=0):
        flag = False;
    return flag;


def checkName(name):
    pattern = '^[A-Za-z]{1,20}$';
    flag = True;
    if re.match(pattern,name, flags=0):
        flag = False;
    return flag;

def checkPassword(password):
    pattern = '^[A-Za-z0-9!@#$%^&*]{8,15}$';
    flag = True;
    if re.match(pattern, password, flags=0):
        flag = False;
    return flag;

def checkFilename(filename):
    pattern = '^[A-Za-z0-9.]{1,15}$';
    flag = True;
    if re.match(pattern, filename, flags=0):
        flag = False;
    return flag;

def checkFileSize(file):
    try :
        flag=False;
        data=file.read();
        file.seek(0);
        return len(data);
    except Exception as e:
        print "Exception : checkFileSize";
        raise e;






