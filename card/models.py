from django.db import models
import account

# Create your models here.
class Word(models.Model):
	word=models.CharField('单词',max_length=50,null=False,primary_key=True)  
	meaning=models.CharField('释义',max_length=200,null=False)
	phonetic=models.CharField('音标',max_length=100,null=False)
	belong=models.CharField('所属词典',max_length=100,null=False)
	class Meta:
		unique_together=("word","belong")
	#time_modified=models.DateField(auto_now=True)

class Lexicon(models.Model):
	name=models.CharField(max_length=200,primary_key=True,default='anonomous') #belong to which list  name=<username>+<wordlist>
	words=models.ManyToManyField(Word, related_name='lexicon')


class CustomizedLexicon(models.Model):
	user=models.ForeignKey(account.models.CustomUser,on_delete=models.CASCADE,related_name='custword')
	word=models.ForeignKey(Word,on_delete=models.CASCADE)
	class Meta:
		unique_together=("user","word")


def validate_range(value):
    if value<0:  # Your desired conditions here
        raise ValidationError('%s some error message' % value)



class UserPlan(models.Model):
	user=models.OneToOneField(account.models.CustomUser,on_delete=models.CASCADE,related_name='userplan',null=False,primary_key=True)  
	amount=models.IntegerField(default=50,validators=[validate_range])

class UserLexicon(models.Model):
	user=models.ForeignKey(account.models.CustomUser,on_delete=models.CASCADE,related_name='userword')
	lexicon=models.ManyToManyField(Word, through='UserWordList')

class UserWordList(models.Model):
	user=models.ForeignKey(UserLexicon,on_delete=models.CASCADE)
	word=models.ForeignKey(Word,on_delete=models.CASCADE)
	is_new=models.BooleanField(default=True)
	count=models.IntegerField(default=0,validators=[validate_range])   #count=10为记住，越小越出现概率越大
	date_modified = models.DateTimeField(auto_now=True)
	date_created = models.DateTimeField(auto_now_add=True)

