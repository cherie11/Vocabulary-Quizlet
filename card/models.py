from django.db import models
import account

# Create your models here.
class Word(models.Model):
	word=models.CharField('单词',max_length=50,null=False,primary_key=True)  
	meaning=models.CharField('释义',max_length=200,null=False)
	phonetic=models.CharField('音标',max_length=100,null=False)
	belong=models.CharField('所属词典',max_length=100,null=False)
	
	#time_finish=models.DateField(auto_now=True)

class Lexicon(models.Model):
	#file=models.FileField(upload_to='File')
	#name=models.CharField(max_length=200)

	name=models.CharField(max_length=200,primary_key=True,default='anonomous') #belong to which list  name=<username>+<wordlist>
	words=models.ManyToManyField(Word, related_name='lexicon')


class CustomizedLexicon(models.Model):
	user=models.ForeignKey(account.models.CustomUser,on_delete=models.CASCADE,related_name='custword')
	words=models.ManyToManyField(Word, related_name='words') #belong to which list  name=<username>+<wordlist>
	

class UserLexicon(models.Model):
	user=models.ForeignKey(account.models.CustomUser,on_delete=models.CASCADE,related_name='userword')
	lexicon=models.ManyToManyField(Word, through='UserWordList')

class UserWordList(models.Model):
	user=models.ForeignKey(UserLexicon,on_delete=models.CASCADE)
	word=models.ForeignKey(Word,on_delete=models.CASCADE)
	is_new=models.BooleanField(default=True)
	count=models.IntegerField(default=0)   #count=10为记住，越小越出现概率越大



