import unittest
from app.models import Comment, Post, User
from app import db

class TestComment(unittest.TestCase):
    def setUp(self):
        self.new_blog = Post(title= 'Test', post= 'Test')
        self.new_comment= Comment(comment='Nice', post= self.new_post)

    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.comment,'Nice')
        self.assertEquals(self.new_comment.post, self.new_post)

    def test_save_comment(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0)

    def test_get_comment_by_blog_id(self):
        self.new_comment.save_comment()
        got_comments = Comment.get_comments(self.new_blog.id)
        self.assertTrue(len(got_comments)==1)

    
    
    
