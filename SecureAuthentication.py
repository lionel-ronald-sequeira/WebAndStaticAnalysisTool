from flask import Flask,render_template,request,redirect,url_for,session,flash
from werkzeug.utils import secure_filename
import EncryptionUtility,FileProcessing,os,ConfigParser,ToolUtility
#import magic
from  datetime import timedelta
from User import User;
from DBOperation import DBOperation;
import InputValidation;
#import flask;

app = Flask(__name__)

#SCRIPT_PATH = os.path.dirname(__file__);
SCRIPT_PATH=os.path.dirname(os.path.abspath(__file__));
#UPLOAD_FOLDER=SCRIPT_PATH+"\\uploads";
UPLOAD_FOLDER="uploads";
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER;
MIME_ALLOWED = set(['text/x-python', 'text/x-php', 'text/x-perl', 'text/x-c']);
EXTENSIONS_ALLOWED=set(['py', 'cpp', 'pl', 'php','c']);

app.permanent_session_lifetime = timedelta(seconds=10);


@app.before_first_request
def initializeConfigurations():

    #flask.session.permanent = True
    #app.permanent_session_lifetime = datetime.timedelta(minutes=20)
    #flask.session.modified = True
    configParser = ConfigParser.RawConfigParser();
    script_path = os.path.dirname(os.path.abspath(__file__));
    filePath = script_path + "\\config.txt";
    configParser.read(filePath);
    app.secret_key=configParser.get('SECRET-key','key');

@app.route('/',methods=['GET','POST'])
def index():
    try :
        if request.method=='GET':
            return render_template("index.html");
        elif request.method=='POST':
            userName = request.form['username'];
            password = request.form['password'];
            inputvalidationmsg = '';
            if (InputValidation.checkUsername(userName)):
                inputvalidationmsg="Username must be 6 to 15 characters can have alphabets,numbers,_ \n";
            if(InputValidation.checkPassword(password)):
                inputvalidationmsg +="Password must be 8 to 15 characters and can have alphabets,numbers,special characters ! @ # $ % ^ & *";
            if inputvalidationmsg != '':
                print "In register";
                flash(inputvalidationmsg);
                return render_template("index.html");
            dbObj=DBOperation();
            dbObj.openConnectionToDB();
            if(dbObj.checkUserExists(userName,None,0)==1):
                passwordsalt=dbObj.getPasswordSaltForUser(userName);
                if(EncryptionUtility.check_password(password,passwordsalt[0],passwordsalt[1])):
                    dbObj.closeConnectionToDb();
                    session['username']=userName;
                    msg='Welcome '+userName;
                    password='';
                    userName='';
                    flash(msg);
                    return redirect("home");
                else :
                    msg="Invalid username or password";
            else:
                msg="Invalid username or password";
            dbObj.closeConnectionToDb();
            flash(msg);
            return render_template("index.html");
    except Exception as e:
        print e;
        flash("Some issue occured");
        return render_template("index.html");

@app.route('/register',methods=['GET','POST'])
def register():
    url="register";
    msg="";
    try :
        if request.method=='GET':
            return render_template("register.html");
        else :
            firstName = request.form['firstname'];
            lastName = request.form['lastname'];
            userName=request.form['username'];
            password=request.form['password'];
            inputvalidationmsg = '';
            if (InputValidation.checkName(firstName)):
                inputvalidationmsg+="Firstname must have alphabets and can have upto 20 characters  \n";
            if(InputValidation.checkName(lastName)):
                inputvalidationmsg+="Lastname must have alphabets and can have upto 20 characters. \n";
            if (InputValidation.checkUsername(userName)):
                inputvalidationmsg += "Username must be 6 to 15 characters and can have alphabets,numbers,_ \n";
            if(InputValidation.checkPassword(password)):
                inputvalidationmsg+="Password must be 8 to 15 characters and can have alphabets,numbers,special characters ! @ # $ % ^ & * \n";
            if inputvalidationmsg !='':
                print "In register";
                flash(inputvalidationmsg);
                return render_template("register.html");

            password_salt_tuple=EncryptionUtility.password_hashing(password,None);
            print(password_salt_tuple[0]);
            print(password_salt_tuple[1]);
            dbObj = DBOperation();
            dbObj.openConnectionToDB();
            if(dbObj.checkUserExists(userName,None,0)==0):
                user = User(firstName, lastName, userName, password_salt_tuple[0], password_salt_tuple[1]);
                dbObj.registerUser(user);
                msg="Welcome "+userName;
                session['username']=userName;
                password='';
                userName='';
                flash(msg);
                return redirect("home");
            else:
                msg="Username already registered";
            dbObj.closeConnectionToDb();
        flash(msg);
        return render_template("register.html");
    except Exception as e:
        print e;
        msg="Some issue occured.";
        flash(msg);
        return render_template("register.html");


@app.route('/home',methods=['GET','POST'])
def home():
    print request.method
    if(session.get('username') is not None):
        return render_template("home.html");
    else :
        return redirect("/");

@app.route('/logout',methods=['GET'])
def logout():
    session.pop('username', None);
    return redirect("/");

@app.route('/uploadfile',methods=['POST'])
def upload_file():
    try:
        print("Start upload file");
        if session.get('username') is None:
            return redirect("/");
        else:
            if 'file' not in request.files:
                flash("File Not Selected");
                return redirect("home");
            file = request.files['file'];
            msg = '';
            print("File.filename :" + file.filename);
            if file.filename == '':
                msg = 'File name must not be blank';
                flash(msg);
                return redirect("home");
            elif InputValidation.checkFilename(file.filename):
                msg='File name can contain alphabets,numbers';
                flash(msg);
                return redirect("home");
            elif InputValidation.checkFileSize(file) > 2000000:
                msg='File must not be greater than 2 MB';
                flash(msg);
                return redirect("home");
            elif InputValidation.checkFileSize(file) ==0:
                msg = 'File size must not be 0';
                flash(msg);
                return redirect("home");
            	#elif file and allowed_file(file.filename):
            elif file and check_mimetype_file(file) and file_allow(file.filename):
                filename = secure_filename(file.filename);
                print("File.filename :" + filename);
                username = session.get('username');
                uploadfolderpath=os.path.join(app.config['UPLOAD_FOLDER']);
                dbObj = DBOperation();
                dbObj.openConnectionToDB();
                FileProcessing.uploadFileToFolder(file,uploadfolderpath,username,filename,dbObj);
                dbObj.closeConnectionToDb();
                msg = 'File uploaded successfully';
                flash(msg);
                return redirect("home");
            else:
                print("Invalid file type");
                msg = 'Invalid file type';
                flash(msg);
                return redirect("home");
    except Exception as e:
        print e;
        msg = "Some issue occured.";
        flash(msg);
        return redirect("home");



    print ("End of upload file");

@app.route('/viewresults',methods=['GET'])
def viewToolResults():
    if session.get('username') is None:
        return redirect("/");
    else :
        resultList=FileProcessing.getToolResults(session.get('username'),os.path.join(app.config['UPLOAD_FOLDER']));
        flash(resultList);
        return render_template("toolresults.html");


def file_allow(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in EXTENSIONS_ALLOWED

def check_mimetype_file(file):
    #mime_type=magic.from_buffer(file.read(1024), mime=True);
    file.seek(0);
    #print mime_type;
    #return mime_type in MIME_ALLOWED;

if __name__ == '__main__':
    app.run()
    ''' To deploy on ec2 add public dns url in host and port will be port no configured while creating ec2 instance '''
    app.run(host='<PUBLIC_DNS_URL>',port='<PORT_NO>',debug=True)