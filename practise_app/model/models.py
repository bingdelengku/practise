# -coding:utf-8-

#创建模型对象

from app import db,login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

class User(UserMixin,db.Model):
    #User继承UserMixin和db.Model类的功能属性
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
###加载用户的回调函数接收以Unicode字符串形式表示的用户标示符
###如果能找到用户，这个函数必须返回用户对象，否则返回None。
def load_user(user_id):
    return User.query.get(int(user_id))

#文章分类
class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self,name):
        self.name = name
    def __repr__(self):
        return '<Category %r>' % self.name

#文章
class Articles(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80))
    author = db.Column(db.String(80))
    content = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)
    reading_number = db.Column(db.Integer)

    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
    category = db.relationship('Category',backref=db.backref('articles',lazy='dynamic'))

    def __init__(self,title,content,reading_number,category,pub_date=None,author='DK'):
        self.title = title
        self.author = author
        self.content = content
        self.reading_number = reading_number
        self.category = category
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date

    def __repr__(self):
        return '<Articles %r>' % self.title


#文章标签
class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer,primary_key=True)
    article_id = db.Column(db.Integer)
    name = db.Column(db.String(50))

    def __init__(self,article_id,name):
        self.article_id = article_id
        self.name = name

    def __repr__(self):
        return '<Tag %r>' % self.name


#文章和标签映射表
class ActMappTags(db.Model):
    __tablename__ = 'actmapptags'
    id = db.Column(db.Integer,primary_key=True)
    article_id = db.Column(db.Integer)
    tag_id = db.Column(db.Integer)

    def __init__(self,article_id,tag_id):
        self.article_id = article_id
        self.tag_id = tag_id

    def __repr__(self):
        return '<ActMappTags %r>' % self.article_id



