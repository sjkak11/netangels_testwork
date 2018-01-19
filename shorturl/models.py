import hashlib
from django.db import models
from django.core.urlresolvers import reverse_lazy


class ConvertedUrl(models.Model):
    short_url = models.CharField('Short url', max_length=128, blank=False)
    original_url = models.URLField('Original url', max_length=512, blank=False)
    created_dt = models.DateTimeField(auto_now=True, verbose_name='Created Date')
    redirect_count = models.PositiveIntegerField('Redirect count', default=0)

    class Meta:
        verbose_name = 'Moder converted url'
        ordering = ('-redirect_count', '-created_dt', )

    def __str__(self):
        return str(self.short_url)

    def save(self, *args, **kwargs):
        self.set_shorturl()
        super().save(*args, **kwargs)

    def set_shorturl(self):
        self.short_url = self.convert_url(self.original_url)

    def convert_url(self, url):
        return hashlib.md5(str(url).encode('utf-8')).hexdigest()

    def get_shorturl(self):
        return self.short_url

    def update_redirect_count(self):
        return self.__class__.objects.filter(id=self.id).update(redirect_count=models.F('redirect_count') + 1)

    def get_absolute_url(self):
        return reverse_lazy('shorturl_detail', kwargs={'pk': self.pk})
