from django.db import models

class Post(models.Model):
    description = models.CharField(max_length = 300, null = True)
    hit         = models.IntegerField(default = 0)
    created_at  = models.DateTimeField(auto_now_add = True)
    updated_at  = models.DateTimeField(auto_now = True)
    living_type = models.ForeignKey('LivingType', on_delete = models.CASCADE)
    space       = models.ForeignKey('Space', on_delete = models.CASCADE)
    size        = models.ForeignKey('Size', on_delete = models.CASCADE)
    style       = models.ForeignKey('Style', on_delete = models.CASCADE)
    user        = models.ForeignKey('users.User', on_delete = models.CASCADE)

    class Meta:
        db_table = 'posts'

    def __str__(self):
        return self.description

class Image(models.Model):
    image_url = models.URLField(max_length = 500)
    post      = models.ForeignKey('Post', on_delete = models.CASCADE)

    class Meta:
        db_table = 'images'

    def __str__(self):
        return self.image_url

class LivingType(models.Model):
    name = models.CharField(max_length = 300)

    class Meta:
        db_table = 'living_types'

    def __str__(self):
        return self.name

class Space(models.Model):
    name = models.CharField(max_length = 300)

    class Meta:
        db_table = 'spaces'

    def __str__(self):
        return self.name

class Size(models.Model):
    name  = models.CharField(max_length = 300) # 수정

    class Meta:
        db_table = 'sizes'

    def __str__(self):
        return self.name

class Style(models.Model):
    name = models.CharField(max_length = 300)

    class Meta:
        db_table = 'styles'

    def __str__(self):
        return self.name

class Like(models.Model):
    post       = models.ForeignKey('Post', on_delete = models.CASCADE)
    user       = models.ForeignKey('users.User', on_delete = models.CASCADE)

    class Meta:
        db_table = 'likes'

class Comment(models.Model):
    content     = models.TextField(max_length = 2000)
    created_at  = models.DateTimeField(auto_now_add = True)
    updated_at  = models.DateTimeField(auto_now = True)
    sub_comment = models.ForeignKey('self', on_delete = models.CASCADE, null = True)
    post        = models.ForeignKey('Post', on_delete = models.CASCADE)
    user        = models.ForeignKey('users.User', on_delete = models.CASCADE)

    class Meta:
        db_table = 'comments'

    def __str__(self):
        return self.content