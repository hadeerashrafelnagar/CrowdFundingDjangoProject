from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from django.db.models import Avg, Sum
from datetime import datetime
from crowdFunding.models import myuser 
from django.template.defaultfilters import slugify

class Categories(models.Model):
    name = models.CharField(max_length=100)

    def project(self):
        return self.project_set.all()

    def __str__(self):
        return self.name


class ProjectTage(models.Model):
    tage = models.CharField(max_length=100, unique=True)

    def project_all(self):
        return self.project_set.all()

    def __str__(self):
        return self.tage


class Project(models.Model):
    title = models.CharField(max_length=100)
    details = models.TextField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    totalTarget = models.IntegerField()
    tags = models.ManyToManyField(ProjectTage, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(myuser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image=models.ImageField(upload_to='images/',default='None/no-img.jpg')

    def first_Projectphoto(self):
        return self.imageproject_set.all().first()

    def allImage(self):
        return self.imageproject_set.all()

    def rating(self):
        return self.rate_set.all().aggregate(Avg('rate'))

    def countrate(self):
        return self.rate_set.all().count()

    def comments(self):
        return self.comment_set.all()

    def commentcount(self):
        return self.comment_set.all().count()

    def donationCount(self):
        return self.donation_set.all().count()
    def donationMoney(self):
        donate=self.donation_set.all().aggregate(Sum('amount'))
        return donate
            # hadeer

    def relativeProject(self):
        num = self.tags.count()
        if num == 1:
            return self.tags.all()[0].project_all()[0:4]
        elif num == 2:
            first = self.tags.all()[0].project_all()[0:2]
            second = self.tags.all()[1].project_all()[0:2]
            return first.union(second)
        elif num == 3:
            first = self.tags.all()[0].project_all()[0:2]
            second = self.tags.all()[1].project_all()[0:1]
            third = self.tags.all()[2].project_all()[0:1]
            return first.union(third, second)
        elif num == 4:
            first = self.tags.all()[0].project_all()[0:1]
            second = self.tags.all()[1].project_all()[0:1]
            third = self.tags.all()[2].project_all()[0:1]
            four = self.tags.all()[3].project_all()[0:1]
            return first.union(third, second, four)
        else:

            return self.tags.all()

    def checkTarget(self):
        if self.donation_set.all().aggregate(Sum('amount'))['amount__sum'] is None:
            return True
        else:
            return (int(self.donation_set.all().aggregate(Sum('amount'))['amount__sum']) / int(
                self.totalTarget)) * 100 < 25

    def getTages(self):
        return self.tags.all()

    def get_date(self):
        time = datetime.now()
        if self.created_at.day == time.day:
            return str(time.hour - self.created_at.hour) + " hours ago"
        if self.created_at.month == time.month:
            return str(time.day - self.created_at.day) + " days ago"
        else:
            if self.created_at.year == time.year:
                return str(time.month - self.created_at.month) + " months ago"

        return self.created_at

    def __str__(self):
        return self.title


class ImageProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    image = models.ImageField(upload_to='images/',default='None/no-img.jpg')


    def remove_on_image_update(self):
        try:
            # is the object in the database yet?
            obj = ImageProject.objects.get(id=self.id)
        except ImageProject.DoesNotExist:
            # object is not in db, nothing to worry about
            return
        # is the save due to an update of the actual image file?
        if obj.image and self.image and obj.image != self.image:
            # delete the old image file from the storage in favor of the new file
            obj.image.delete()

    def delete(self):
        # object is being removed from db, remove the file from storage first
        self.image.delete()
        return super(ImageProject, self).delete( )

    def save(self):
        # object is possibly being updated, if so, clean up.
        self.remove_on_image_update()
        return super(ImageProject, self).save()
    def __str__(self):
        return f"photo of :{self.project}"
    
def get_image_filename(instance, filename):
    title = instance.post.title
    slug = slugify(title)
    return "post_images/%s-%s" % (slug, filename)

class Rate(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(myuser, on_delete=models.CASCADE)
    rate = models.IntegerField(validators=[MinValueValidator(1)
        , MaxValueValidator(10)])
    def __str__(self):
        return f"rate of {self.project} : {self.rate}"

class FeatureProjects(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def save(self):
        if FeatureProjects.objects.count() == 5:
            FeatureProjects.objects.all()[0].delete()

        super(FeatureProjects, self).save()
    def __str__(self):
        return self.project.title

class Donation(models.Model):
    owner = models.ForeignKey(myuser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.project} -{self.owner}"

class Comment(models.Model):
    user = models.ForeignKey(myuser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def get_date(self):
        time = datetime.now()
        if self.created_at.day == time.day:
            return str(time.hour - self.created_at.hour) + " hours ago"
        if self.created_at.month == time.month:
            return str(time.day - self.created_at.day) + " days ago"
        else:
            if self.created_at.year == time.year:
                return str(time.month - self.created_at.month) + " months ago"

        return self.created_at

    def __str__(self):
        return self.content



class ReportComment(models.Model):
    user = models.ForeignKey(myuser, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    # hadeer
class ReportProject(models.Model):
    user = models.ForeignKey(myuser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
    # hadeer
