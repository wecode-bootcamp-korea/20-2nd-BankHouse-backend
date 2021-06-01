from django.db import models

class User(models.Model):
    email            = models.CharField(max_length = 500)
    password         = models.CharField(max_length = 500, null = True)
    kakao_id         = models.CharField(max_length = 500, null = True) 

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email

class UserInformation(models.Model):
    nickname  = models.CharField(max_length = 300)
    is_expert = models.BooleanField(default = False)
    image_url = models.URLField(max_length = 500, null = True)
    user      = models.ForeignKey('User', on_delete = models.CASCADE)

    class Meta:
        db_table = 'user_informations'

    def __str__(self):
        return self.nickname