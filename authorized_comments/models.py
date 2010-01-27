from django.contrib.comments.models import Comment

class AuthorizedComment(Comment):
    #TODO: Fix this today: 

    def get_flag_url(self):
        return "/auth_comments/flag/%s/" % self.id

    def get_delete_url(self):
        return "/auth_comments/delete/%s/" % self.id

