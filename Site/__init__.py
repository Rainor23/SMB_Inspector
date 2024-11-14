from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

DB_NAME = str(input("Type name for database: "))

app.config['SECRET_KEY']  = 'Smbtestingletsgo'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}.db'
db = SQLAlchemy()

db.init_app(app)

@app.route('/')
def report():
    share_scan_count = SMBShare.query.count()
    interesting_count = File.query.count()
    dangerous_count = FileDanger.query.count()
    list_interesting = File.query.all()
    list_dangerous = FileDanger.query.all()
    return render_template("dashboard.html", title="Report", share_scan_count=share_scan_count, interesting_count=interesting_count, dangerous_count=dangerous_count, list_interesting=list_interesting, list_dangerous=list_dangerous)

class SMBShare(db.Model):
    __tablename__ = 'smb_shares'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    files = db.relationship('File', backref='smb_share', lazy=True)
    danger = db.relationship('FileDanger', backref='smb_share', lazy=True)


class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(1024), nullable=False) 
    smb_share_name = db.Column(db.String, db.ForeignKey('smb_shares.name'), nullable=False)

    permissions = db.relationship('Permission', backref='file', lazy=True)

class FileDanger(db.Model):
    __tablename__ = 'dangerous'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(1024), nullable=False) 
    dangerous_permission = db.Column(db.String(1024), nullable=False) 
    smb_share_name = db.Column(db.String, db.ForeignKey('smb_shares.name'), nullable=False)

    #permissions = db.relationship('Permission', backref='file', lazy=True)

class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'), nullable=False)
    user_or_group = db.Column(db.String(255), nullable=False)
    permission_type = db.Column(db.String(50), nullable=False)

def add_share(sharename):
    with app.app_context():
        db.session.add(SMBShare(name=sharename))
        db.session.commit()
        

def add_file(filepath, sharename):
    with app.app_context():
        share = SMBShare.query.filter_by(name=sharename).first()
        db.session.add(File(path=filepath, smb_share=share))
        db.session.commit()

def add_dangerous(filepath, permission, sharename):
    with app.app_context():
        share = SMBShare.query.filter_by(name=sharename).first()
        db.session.add(FileDanger(path=filepath, dangerous_permission=permission, smb_share=share))
        db.session.commit()


with app.app_context():
    db.create_all()