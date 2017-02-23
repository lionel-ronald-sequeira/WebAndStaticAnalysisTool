class User:

    firstName=None;
    lastName=None;
    userName=None;
    password=None;
    salt=None;

    def __init__(self,firstName,lastName,userName,password,salt):
        print "User constructor";
        self.firstName=firstName;
        self.lastName=lastName;
        self.userName=userName;
        self.salt = salt;
        self.password=password;


