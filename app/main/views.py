from os import abort
from flask import  render_template, url_for, flash, redirect, abort
from . import main
from .forms import CommentForm, AddPost, LoginForm, UpdateProfile
from app.models import User,Post, Comments, Votes
from flask_login import login_required, current_user
from ..request import get_quotes
from ..import db


@main.route("/")
# @main.route("/home")
def home():

    posts = Post.query.all()

    quote = get_quotes()


    return render_template('home.html', posts=posts, quote = quote) 


@main.route("/about")
def about():

    return render_template('about.html', title = 'About')


#.....
@main.route('/user/<uname>')
@login_required
def profile(uname):

    img_file =url_for('static', filename='current_user.')
    user = User.query.filter_by(username = uname).first()

    if user is None:

        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):

    user = User.query.filter_by(username = uname).first()
    if user is None:

        abort(404)

    form = UpdateProfile()
    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/posts/new', methods = ['GET','POST'])
@login_required
def new_post():
    form = AddPost()
    if form.validate_on_submit():
        
        # author = current_user.id
        new_post = Post(title = form.title.data, content= form.content.data, user_id = current_user.id)
        db.session.add(new_post)
        db.session.commit()

        flash(f'Your post was created succesfully !', 'success')

        return redirect(url_for('main.home'))

    return render_template('auth/addpost.html',form=form)


#adding a comment
@main.route('/write_comment/<int:id>', methods=['GET', 'POST'])
@login_required
def post_comment(id):
    """ 
    Function to post comments 
    """
    
    form = CommentForm()
    title = 'post comment'
    post = Post.query.filter_by(id=id).first()

    if post is None:

         abort(404)

    if form.validate_on_submit():
        comment = form.comment.data
        new_comment = Comments(opinion = comment, user_id = current_user.id, posts_id = post.id)
        new_comment.save_comment()
        return redirect(url_for('main.view_post', id = post.id))

    return render_template('comments.html', form = form, title = title)


#view single post alongside its comments
@main.route('/view-post/<int:id>', methods=['GET', 'POST'])
@login_required
def view_post(id):
    """
    Function the returns a single post for a comment to be added
    """
    # all_category = postCategory.get_categories()
    posts = Post.query.get(id)

    if posts is None:

        abort(404)
    
    comment = Comments.get_comments(id)
    print(comment)
    count_likes = Votes.query.filter_by(posts_id=id, vote=1).all()
    count_dislikes = Votes.query.filter_by(posts_id=id, vote=2).all()
    return render_template('view-post.html', posts = posts, comment = comment, count_likes=len(count_likes), count_dislikes=len(count_dislikes))


#Routes upvoting/downvoting postes
@main.route('/post/upvote/<int:id>&<int:vote_type>')
@login_required
def upvote(id,vote_type):
    """
    View function that adds one to the vote_number column in the votes table
    """
    # Query for user
    votes = Votes.query.filter_by(user_id=current_user.id).all()
    to_str=f'{vote_type}:{current_user.id}:{id}'

    if not votes:
        new_vote = Votes(vote=vote_type, user_id=current_user.id, posts_id=id)
        new_vote.save_vote()
        flash('YOU HAVE VOTED', 'success')

    for vote in votes:
        if f'{vote}' == to_str:

            break
        else:   
            new_vote = Votes(vote=vote_type, user_id=current_user.id, posts_id=id)
            new_vote.save_vote()
           
            break

    return redirect(url_for('.view_post', id=id))


#Update post
@main.route('/view-post/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_post(id):

    post = Post.query.get_or_404(id)
    if post.user_id != current_user.id:
        abort(403)

    form = AddPost()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()

        flash('Your Post has been updated succesfull', 'success')

        return redirect(url_for('main.view_post', id = post.id))

    form.title.data =post.title
    form.content.data = post.content 

    return render_template('auth/addpost.html',form=form , title= 'Update Post')




#Update post
@main.route('/view-post/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(id):

    post = Post.query.get_or_404(id)
    if post.user_id != current_user.id:
        abort(403)
    db.session.delete(post)
    db.session.commit()

    flash('Your post has been deleted', 'success')

    return redirect(url_for('main.home'))

    