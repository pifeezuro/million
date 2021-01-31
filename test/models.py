from django.db import models

# Create your models here.
from django.utils import timezone


class Tag(models.Model):
    tag = models.CharField('タグ名', max_length=50)

    def __str__(self):
        return self.tag


class Post(models.Model):
    title = models.CharField('タイトル', max_length=35)
    text = models.TextField('本文')
    image = models.ImageField('画像', upload_to='images', blank=True)
    created_at = models.DateTimeField('投稿日', default=timezone.now)
    tag = models.ForeignKey(Tag, verbose_name='タグ', on_delete=models.PROTECT)

    def __str__(self):
        return self.title
