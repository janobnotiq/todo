from django.db import models
from django.contrib.auth.models import User
from config.models import BaseModel



class Category(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"


class Task(BaseModel):
    task = models.CharField(max_length=300)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="categories")
    doer = models.ForeignKey(User,on_delete=models.CASCADE,related_name="users")
    is_done = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.task[:10] + "..."
    
    class Meta:
        ordering = ['-updated_at',]
    

class Comment(BaseModel):
    
    class StarChoices(models.TextChoices):
        BIR = "BIR","BIR"
        IKKI = "IKKI","IKKI"
        UCH = "UCH","UCH"
        TORT = "TORT","TORT"
        BESH = "BESH","BESH"
    
    author = models.OneToOneField(User,on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Izoh")
    stars = models.CharField(max_length=5,choices=StarChoices.choices,verbose_name="Yulduzchalar")

    def __str__(self) -> str:
        return f"{self.author.username}ning izohi"
    
    class Meta:
        ordering = ["-updated_at",]    