from django.db import models
from companies.models import FieldOfActivity, Company, City, Province
from django.contrib.auth import get_user_model
User = get_user_model()


class Skill(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Ad(models.Model):
    TYPE_OF_COOPERATION = (
        ('تمام وقت', 'تمام وقت'),
        ('پاره وقت', 'پاره وقت'),
        ('کارآموزی', 'کارآموزی'),
        ('دورکاری', 'دورکاری')
    )

    WORK_EXPERIENCE = (
        ('بدون محدودیت سابقه کار', 'بدون محدودیت سابقه کار'),
        ('کمتر از سه سال', 'کمتر از سه سال'),
        ('سه تا شش سال', 'سه تا شش سال'),
        ('بیش از شش سال', 'بیش از شش سال')
    )
    SALARY = (
        ('توافقی', 'توافقی'),
        ('حقوق پایه(وزارت کار)', 'حقوق پایه(وزارت کار)'),
        ('از چهار میلیون و پانصد هزار تومان', 'از چهار میلیون و پانصد هزار تومان'),
        ('از پنج میلیون تومان', 'از پنج میلیون تومان'),
        ('از هفت میلیون تومان', 'از هفت میلیون تومان'),
        ('از هشت میلیون تومان', 'از هشت میلیون تومان'),
        ('از ده میلیون تومان', 'از ده میلیون تومان'),
        ('از دوازده میلیون تومان', 'از دوازده میلیون تومان'),
        ('از پانزده میلیون تومان', 'از پانزده میلیون تومان'),
        ('از بیست میلیون تومان', 'از بیست میلیون تومان'),
        ('از سی و پنج میلیون تومان', 'از سی و پنج میلیون تومان'),
        ('از پنجاه میلیون تومان', 'از پنجاه میلیون تومان')
    )

    title = models.CharField(max_length=100)
    category = models.ForeignKey(FieldOfActivity, on_delete=models.CASCADE, related_name='ads')
    type_of_cooperation = models.CharField(max_length=70, choices=TYPE_OF_COOPERATION)
    work_experience = models.CharField(max_length=100, choices=WORK_EXPERIENCE)
    salary = models.CharField(max_length=100, choices=SALARY)
    description = models.TextField()
    skill = models.ManyToManyField(Skill, related_name='ads')
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='ads')
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='ads')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='ads')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Resume(models.Model):
    class ResumeStatus(models.TextChoices):
        SENT = 'ارسال به کارفرما', 'ارسال به کارفرما'
        REVIEWED = 'بررسی شده', 'بررسی شده'
        INTERVIEW = 'مصاحبه', 'مصاحبه'
        REJECT = 'رد شده', 'رد شده'
        RECRUITMENT = 'استخدام', 'استخدام'

    job_seeker = models.OneToOneField(User, on_delete=models.CASCADE, related_name='resume')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='resumes')
    status = models.CharField(max_length=90, choices=ResumeStatus.choices)
    file = models.FileField(upload_to='media/resumes_files/')
    phone_number = models.CharField(max_length=11)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job_seeker', 'ad')

    def send_resume(self):
        self.status = Resume.ResumeStatus.SENT
        self.save()

    def review_resume(self):
        self.status = Resume.ResumeStatus.REVIEWED
        self.save()

    def interview(self):
        self.status = Resume.ResumeStatus.INTERVIEW
        self.save()
    
    def response(self, response):
        if response == 'accept':
            self._recruitment()
        elif response == 'reject':
            self._reject()

    def _recruitment(self):
        self.status = Resume.ResumeStatus.RECRUITMENT
        self.save()

    def _reject(self):
        self.status = Resume.ResumeStatus.REJECT
        self.save()

    def __str__(self):
        return f'{self.job_seeker.email} resume'


class Save(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saves')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='saves')

    def __str__(self):
        return f'{self.user.email} saved ad:{self.ad.title}'

