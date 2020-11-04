from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from datetime import datetime
from flask_login import UserMixin
from . import login_manager


class User(UserMixin, db.Model):
    """ 
    class modelling the users 
    """

    __tablename__='users'

    #create the columns
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True, index =True)
    pass_secure = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String(20), default='default.jpeg')
    posts = db.relationship("Post", backref="user", lazy = "dynamic")
    comment = db.relationship("Comments", backref="user", lazy = "dynamic")
    vote = db.relationship("Votes", backref="user", lazy = "dynamic")

  

    # securing passwords
    @property
    def password(self):
        raise AttributeError('You can not read the password Attribute')


    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)


    def __repr__(self):
        return f'User {self.username}'


#posts class
class Post(db.Model):
    """
    List of posts in each category 
    """

    __tablename__ = 'posts'

    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String())
    content = db.Column(db.String())
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comment = db.relationship("Comments", backref="posts", lazy = "dynamic")
    vote = db.relationship("Votes", backref="posts", lazy = "dynamic")


    


    def save_post(self):
        """
        Save the posts 
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def clear_posts(cls):
        Post.all_posts.clear()

    # display posts

    def get_posts(id):
        post = Post.query.filter_by(category_id=id).all()

        return post



# comments
class Comments(db.Model):
    """
    User comment model for each pitch 
    """

    __tablename__ = 'comments'

    # add columns
    id = db.Column(db. Integer, primary_key=True)
    opinion = db.Column(db.String(255))
    time_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    posts_id = db.Column(db.Integer, db.ForeignKey("posts.id"))


    def save_comment(self):
        """
        Save the Comments/comments per pitch
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(self, id):
        comment = Comments.query.filter_by(posts_id=id).all()
        
        return comment


#votes
class Votes(db.Model):
    """
    class to model votes
    """
    __tablename__='votes'

    id = db.Column(db. Integer, primary_key=True)
    vote = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    posts_id = db.Column(db.Integer, db.ForeignKey("posts.id"))

    def save_vote(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    
    def get_votes(cls,user_id, posts_id):
        votes = Votes.query.filter_by(user_id=user_id, posts_id= posts_id).all()
        return votes




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


