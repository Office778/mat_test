from django.db import models


# Create your models here.
class Customers(models.Model):
    cus_id = models.CharField(max_length=100)
    cus_name = models.CharField(max_length=100)
    cus_mobile = models.CharField(max_length=100)
    cus_email = models.CharField(max_length=100)
    cus_password = models.CharField(max_length=100)
    image_name = models.CharField(max_length=255, blank=True, null=True)
    image_type = models.CharField(max_length=50, blank=True, null=True)
    image_path = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    haroscope_file_path = models.CharField(max_length=100)
    trust_file_path = models.CharField(max_length=100)
    profile_for = models.CharField(max_length=100)
    name_for = models.CharField(max_length=100)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=100)
    religion = models.CharField(max_length=100)
    mothertongue = models.CharField(max_length=100)
    caste = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    marital_status = models.CharField(max_length=100)
    diet = models.CharField(max_length=100)
    height = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    work = models.CharField(max_length=100)
    discription = models.CharField(max_length=200)
    cus_credits = models.IntegerField()
    trust_mark = models.IntegerField()
    switch_1 = models.IntegerField()
    switch_2 = models.IntegerField()
    t_c = models.CharField(max_length=100)
    last_login = models.DateTimeField()
    trn_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'customers'

class Options(models.Model):
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'options'
    
class Plan(models.Model):
    plan = models.CharField(max_length=100)
    amt = models.CharField(max_length=100)
    credit = models.CharField(max_length=100)

    class Meta:
        managed = False  # Django won't manage this table
        db_table = 'plan'  # Map to existing table in the database


class HistoryTran(models.Model):
    date = models.DateTimeField()
    cus_id = models.IntegerField()
    tran_no = models.CharField(max_length=100)
    plan = models.CharField(max_length=100)
    amt = models.IntegerField()
    credit = models.IntegerField()
    emp_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'history_tran'

class HistoryUnlock(models.Model):
    date = models.DateTimeField()
    cus_id = models.CharField(max_length=100)
    cus_unlock_ids = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'history_unlock'
        

class Blog(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    des = models.CharField(max_length=10000)
    blog_img_name = models.CharField(max_length=100)
    blog_img_path = models.CharField(max_length=100)
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'blog'