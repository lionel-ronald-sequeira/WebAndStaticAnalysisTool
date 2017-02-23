from pymongo import MongoClient
import ConfigParser, os
class DBOperation:

    client=None;
    db=None;

    def __init__(self):
        print ("In db object");

    def openConnectionToDB(self):
        try :
            print "Start Open connection to db";
            configParser=ConfigParser.RawConfigParser();
            script_path=os.path.dirname(os.path.abspath(__file__));
            filePath=script_path+"\\config.txt";
            configParser.read(filePath);
            #configParser.read('config.txt');
            username=configParser.get('DB-config','username');
            password=configParser.get('DB-config','password');
            url=configParser.get('DB-config','url');
            dbname=configParser.get('DB-config','dbname');
            dbpath="mongodb://"+username+":"+password+"@"+url+"/"+dbname;
            self.client=MongoClient(dbpath);
            self.db = self.client.secure_program;
            print "End Open connection to db";
        except Exception:
            print "Exception : openConnectionToDB";
            raise Exception;

    def closeConnectionToDb(self):
        try :
            self.client.close();
        except Exception:
            print "Exception : closeConnectionToDb";

    def registerUser(self,user):
        print "Start of register user";
        try :
            userDetails={"first_name":user.firstName,"last_name":user.lastName,"user_name":user.userName,
                         "pass_word":user.password,"salt":user.salt};
            self.db.user_details.insert_one(userDetails);
        except Exception as e:
            if self.client != None:
                self.closeConnectionToDb();
            print "Exception : registerUser";
            raise e;

    def checkUserExists(self,username,password,filtercheck):
        count=0;
        print "In check user exists";
        try :
            if filtercheck :
                count=self.db.user_details.count({"user_name":username,"pass_word":password});
            else :
                count=self.db.user_details.count({"user_name":username});
            print "Count of record",count;
            return count;
        except Exception as e:
            if self.client != None:
                self.closeConnectionToDb();
            print "Exception : checkUserExists";
            raise e;

    def getPasswordSaltForUser(self,username):
        print "Start getPasswordSaltForUser";
        salt='';
        try:
            row=self.db.user_details.find({"user_name":username});
            for c in row:
                return (c["pass_word"],c["salt"]);
            print "End getPasswordSaltForUser";
        except Exception as e:
            if self.client != None:
                self.closeConnectionToDb();
            print "Exception : getPasswordSaltForUser";
            raise e;

    def storeToolResult(self,fileName,userName,toolResult,toolName,resultfileName):
        print "Start storeToolResult";
        try:
            toolResults = {"user_name": userName, "file_name": fileName, "tool_result": toolResult,"tool_name":toolName,"result_file_name":resultfileName};
            self.db.tool_results.insert_one(toolResults);

        except Exception as e:
            if self.client != None:
                self.closeConnectionToDb();
            print "Exception : storeToolResult";
            raise e;
        print "End storeToolResult";

    def updateToolResult(self,fileName,resultfileName,userName,toolResult):
        print "Start updateToolResult";
        try:
            if fileName ==None:
                self.db.tool_results.update(
                    {"user_name": userName, "result_file_name": resultfileName},
                    {"$set": {"tool_result": toolResult}});
            else:
                self.db.tool_results.update({"user_name":userName,"file_name":fileName,"result_file_name":resultfileName,"tool_result":""},{"$set":{"tool_result":toolResult}});
        except Exception as e:
            if self.client != None:
                self.closeConnectionToDb();
                print "Exception : updateToolResult";
            raise e;
        print "End updateToolResult";

    def getToolResult(self,userName):
        print "Start getToolResult";
        try:
            resultList=[];
            row = self.db.tool_results.find({"user_name": userName});
            for c in row:
                print c["file_name"] + c["tool_name"] + c["tool_result"];
                resultList.append((c["file_name"] ,c["tool_name"] ,c["tool_result"]));
            return resultList;
        except Exception as e:
            if self.client != None:
                self.closeConnectionToDb();
                print "Exception : getToolResult";
            raise e;
        print "End getToolResult";
