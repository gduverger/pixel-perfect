from django.db import models


class Test(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    browserstack_job_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    file = models.FileField(upload_to='mocks')
    link = models.URLField(max_length=500)

    def __str__(self):
        return u'%s, %s, %s, %s, %s' % (self.id, self.name, self.browserstack_job_id, self.file, self.link)


class Screenshot(models.Model):
    test = models.ForeignKey(Test, related_name='screenshots')
    browserstack_screenshot_id = models.CharField(max_length=50, unique=True)
    browserstack_screenshot_thumb_url = models.CharField(max_length=100)
    browserstack_screenshot_image_url = models.CharField(max_length=100)

    def __str__(self):
        return u'%s, %s, %s, %s, %s' % (self.id, self.test, self.browserstack_screenshot_id, self.browserstack_screenshot_thumb_url, self.browserstack_screenshot_image_url)
