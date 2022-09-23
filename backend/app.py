
from flask import Flask, jsonify, request, escape
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import datetime
import os
import requests
from google.oauth2 import id_token
from pip._vendor import cachecontrol
import google.auth.transport.requests
import pathlib
from flask import Flask, session, abort, redirect, request
from google_auth_oauthlib.flow import Flow
from flask_login import current_user

app = Flask(__name__)
app = Flask("Google Login App")
app.secret_key = "Codespecialist.com"
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/myproject'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "311655855070-51feajk8ejgkboti50j9tsjs91run7a2.apps.googleusercontent.com"
client_secrets_file = os.path.join(
    pathlib.Path(__file__).parent, "Client_secret.json")

flow = Flow.from_client_secrets_file(client_secrets_file=client_secrets_file,
                                     scopes=["https://www.googleapis.com/auth/userinfo.profile",
                                             "https://www.googleapis.com/auth/userinfo.email", "openid"],
                                     redirect_uri="http://127.0.0.1:5000/callback"
                                     )


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)
        else:
            return function()

    return wrapper


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Member = db.Column(db.String(100))
    Date = db.Column(db.DateTime)
    PropertyType = db.Column(db.Text)
    PropertyCondition = db.Column(db.Text)
    PropertyFor = db.Column(db.Text)
    Address = db.Column(db.Text)
    PostalCode = db.Column(db.Text)
    Country = db.Column(db.Text)
    TotalArea = db.Column(db.Text)
    Cost = db.Column(db.Text)
    Comments = db.Column(db.Text)


def __init__(self, Member, Date, PropertyType, PropertyCondition, PropertyFor, Address, PostalCode, Country, TotalArea, Cost, Comments):
    self.Member = Member
    self.Date = Date
    self.PropertyType = PropertyType
    self.PropertyCondition = PropertyCondition
    self.PropertyFor = PropertyFor
    self.Address = Address
    self.PostalCode = PostalCode
    self.Country = Country
    self.TotalArea = TotalArea
    self.Cost = Cost
    self.Comments = Comments


class ArticleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'Member', 'Date', 'PropertyType', 'PropertyCondition', 'PropertyFor',
                  'Address', 'PostalCode', 'Country', 'TotalArea', 'Cost', 'Comments')


article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)


@app.route('/articles/get', methods=['GET'])
def get_articles():
    all_articles = Articles.query.all()
    results = articles_schema.dump(all_articles)
    return jsonify(results)


@app.route('/articles/add', methods=['POST'])
def create_articles():

    Member = request.json['Member']
    Date = request.json['Date']
    PropertyType = request.json['PropertyType']
    PropertyCondition = request.json['PropertyCondition']
    PropertyFor = request.json['PropertyFor']
    Address = request.json['Address']
    PostalCode = request.json['PostalCode']
    Country = request.json['Country']
    TotalArea = request.json['TotalArea']
    Cost = request.json['Cost']
    Comments = request.json['Comments']

    articles = Articles(Member=Member, Date=Date, PropertyType=PropertyType, PropertyCondition=PropertyCondition,
                        PropertyFor=PropertyFor, Address=Address, PostalCode=PostalCode, Country=Country, TotalArea=TotalArea, Cost=Cost, Comments=Comments)

    db.session.add(articles)
    db.session.commit()
    return article_schema.jsonify(articles)


class added_properties(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    ProjectName = db.Column(db.String(100))
    ProjectIncludes = db.Column(db.String(100))
    Address = db.Column(db.Text)
    PostalCode = db.Column(db.Text)
    Country = db.Column(db.Text)


def __init__(self, ProjectName, ProjectIncludes, Address, PostalCode, Country):
    self.ProjectName = ProjectName
    self.ProjectIncludes = ProjectIncludes
    self.Address = Address
    self.PostalCode = PostalCode
    self.Country = Country


class AddedPropertiesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'ProjectName', 'ProjectIncludes',
                  'Address', 'PostalCode', 'Country')


property_schema = AddedPropertiesSchema()
properties_schema = AddedPropertiesSchema(many=True)


@app.route('/properties/get', methods=['GET'])
def get_properties():
    all_properties = added_properties.query.all()
    results = properties_schema.dump(all_properties)
    return jsonify(results)


@app.route('/properties/add', methods=['POST'])
def create_properties():

    ProjectName = request.json['ProjectName']
    ProjectIncludes = request.json['ProjectIncludes']
    Address = request.json['Address']
    PostalCode = request.json['PostalCode']
    Country = request.json['Country']

    properties = added_properties(ProjectName=ProjectName, ProjectIncludes=ProjectIncludes,
                                  Address=Address, PostalCode=PostalCode, Country=Country)

    db.session.add(properties)
    db.session.commit()
    return property_schema.jsonify(properties)


class add_user(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(100))
    About = db.Column(db.String(100))
    Address = db.Column(db.Text)
    PostalCode = db.Column(db.Text)
    Country = db.Column(db.Text)
    Mobile = db.Column(db.Text)


def __init__(self, UserName, About, Address, PostalCode, Country, Mobile):
    self.UserName = UserName
    self.About = About
    self.Address = Address
    self.PostalCode = PostalCode
    self.Country = Country
    self.Mobile = Mobile


class AddUserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'UserName', 'About',
                  'Address', 'PostalCode', 'Country', 'Mobile')


user_schema = AddUserSchema()
users_schema = AddUserSchema(many=True)


@app.route('/users/get', methods=['GET'])
def get_users():
    all_users = add_user.query.all()
    results = users_schema.dump(all_users)
    return jsonify(results)


@app.route('/users/add', methods=['POST'])
def create_users():

    UserName = request.json['UserName']
    About = request.json['About']
    Address = request.json['Address']
    PostalCode = request.json['PostalCode']
    Country = request.json['Country']
    Mobile = request.json['Mobile']

    users = add_user(UserName=UserName, About=About,
                     Address=Address, PostalCode=PostalCode, Country=Country, Mobile=Mobile)

    db.session.add(users)
    db.session.commit()
    return user_schema.jsonify(users)


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(100))
    About = db.Column(db.String(100))
    Address = db.Column(db.Text)
    PostalCode = db.Column(db.Text)
    Country = db.Column(db.Text)
    Mobile = db.Column(db.Text)
    UserType = db.Column(db.Text)


def __init__(self, UserName, About, Address, PostalCode, Country, Mobile, UserType):
    self.UserName = UserName
    self.About = About
    self.Address = Address
    self.PostalCode = PostalCode
    self.Country = Country
    self.Mobile = Mobile
    self.UserType = UserType


class AddUserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'UserName', 'About',
                  'Address', 'PostalCode', 'Country', 'Mobile', 'UserType')


user1_schema = AddUserSchema()
users1_schema = AddUserSchema(many=True)


@app.route('/user/get', methods=['GET'])
def get_user():
    all_user = User.query.all()
    results = users1_schema.dump(all_user)
    return jsonify(results)


@app.route('/user/add', methods=['POST'])
def create_user():

    UserName = request.json['UserName']
    About = request.json['About']
    Address = request.json['Address']
    PostalCode = request.json['PostalCode']
    Country = request.json['Country']
    Mobile = request.json['Mobile']
    UserType = request.json['UserType']

    user = User(UserName=UserName, About=About,
                Address=Address, PostalCode=PostalCode, Country=Country, Mobile=Mobile, UserType=UserType)

    db.session.add(user)
    db.session.commit()
    return user1_schema.jsonify(user)


class Profile(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Picture = db.Column(db.Text)
    Email = db.Column(db.Text)
    Familyname = db.Column(db.Text)


def __init__(self, Name, Picture, Email, Familyname):
    self.Name = Name
    self.Picture = Picture
    self.Email = Email
    self.Familyname = Familyname


class AddProfileSchema(ma.Schema):
    class Meta:
        fields = ('id', 'Name', 'Picture',
                  'Email', 'Familyname')


profile_schema = AddProfileSchema()
profiles_schema = AddProfileSchema(many=True)


@app.route('/profile/get', methods=['GET'])
def get_profile():
    all_profile = Profile.query.all()
    results = profiles_schema.dump(all_profile)
    return jsonify(results)


@app.route('/profile/add', methods=['POST'])
def create_profile():

    Name = request.json['Name']
    Picture = request.json['Picture']
    Email = request.json['Email']
    Familyname = request.json['Familyname']

    profile = Profile(Name=Name, Picture=Picture,
                      Email=Email, Familyname=Familyname)

    db.session.add(profile)
    db.session.commit()
    return profile_schema.jsonify(profile)


@app.route("/auth/google/signup", methods=["POST"])
def auth_google():
    id_info = request.json["id_info"]
    print(id_info)
    return jsonify({"message": "success"})


class Login(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(100))
    Password = db.Column(db.String(100))
    LoginType = db.Column(db.String(100))


def __init__(self, UserName, Password, LoginType, Date_Time):
    self.UserName = UserName
    self.Password = Password
    self.LoginType = LoginType
    self.Date_Time = Date_Time


class AddLoginSchema(ma.Schema):
    class Meta:
        fields = ('id', 'UserName', 'Password', 'LoginType', 'Date_Time')


login_schema = AddLoginSchema()
logins_schema = AddLoginSchema(many=True)


@app.route('/login/get', methods=['GET'])
def get_login():
    all_login = Login.query.all()
    results = logins_schema.dump(all_login)
    return jsonify(results)


@app.route('/login/add', methods=['POST'])
def create_login():

    UserName = request.json['UserName']
    Password = request.json.get('Password', "NO_PASSWORD")
    LoginType = request.json["LoginType"]
    Date_Time = request.json["Date_Time"]

    login = Login(UserName=UserName, Password=Password,
                  LoginType=LoginType, Date_Time=Date_Time)

    db.session.add(login)
    db.session.commit()
    return login_schema.jsonify(login)


@app.route("/signin")
def login():
    print("entering login function")
    authorization_url, state = flow.authorization_url()
    print(authorization_url)
    session["state"] = state
    print(state)
    print("exiting login function")
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    print("entering callback function")
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(
        session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    print("exiting callback function")
    print(id_info)
    profile = Profile(Name=id_info.get("name"), Picture=id_info.get("picture"),
                      Email=id_info.get("email"), Familyname=id_info.get("family_name"))

    db.session.add(profile)
    db.session.commit()
    return redirect("/protected_area")


@app.route("/signout")
def signout():
    count = session.get("name")
    print(count)
    return count


@app.route("/logout")
def logout():
    session.clear()
    return redirect('http://localhost:3000/LoginApi')


@app.route("/index")
def index():
    return "<a href = '/signin'><button>Login</button></a>"


@app.route("/protected_area")
@login_is_required
def protected_area():
    print("entering protected function")
    print("exiting protected function")
    return redirect('http://localhost:3000/Link')


if __name__ == "__main__":
    app.run(debug=True)
