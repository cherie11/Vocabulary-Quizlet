from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.template import Library
from .forms import *
from .models import Lexicon,Word,UserWordList,UserLexicon
from django.core.files.storage import FileSystemStorage
import xlrd 
from django.views.generic import TemplateView
from django.http import Http404,JsonResponse
from django.shortcuts import render
import account
from django.views.decorators.csrf import csrf_exempt
import random

#from django.contrib.auth.decorators import login_required

#@login_required
class UploadWordsView(TemplateView):
	template_name = 'home.html'

	def post(self, request, *args, **kwargs):
		context = self.get_context_data()
		saved=False

		print(context)
		if form.is_valid():
			wb=xlrd.open_workbook(filename=None,file_contents=request.FILES.get('lexicon').read())
			table=wb.sheets()[0]
			row=table.nrows
			lexicon = Lexicon()
			lexicon.name=context["lexicon"].cleaned_data["name"]
			lexicon.save()
			for i in range(row):
				word=Word(word=table.row_values(i)[1],meaning=table.row_values(i)[2],phonetic=table.row_values(i)[3])
				word.save()
				lexicon.words.add(word)
			lexicon.save()
			saved = True
            #save your model
            #redirect
		
		return super(TemplateView, self).render_to_response(context)

	def get_context_data(self, **kwargs):
		context = super(UploadWordsView, self).get_context_data(**kwargs)
		if self.request.method=='POST':
			form = LexiconForm(self.request.POST,self.request.FILES)  # instance= None

		else:
			form=LexiconForm()
		context['cur_user'] = self.request.user

		context['lexicon'] = form
		return context

#@login_required
def detail(request,slug,known,**kwargs):
	if request.method == 'GET':
		userword=UserWordList.objects.filter(user__user__email=request.user,is_new=True,word__word__in=Word.objects.filter(belong=slug))	
				#userword=userwords.objects.filter(belong=slug)
		if(userword.count()!=0):
			word=userword[0].word
		else:
			userword=UserWordList.objects.filter(user__user__email=request.user,is_new=False,word__word__in=Word.objects.filter(belong=slug)).order_by('-count')
			word=userword[0].word


	elif request.method == 'POST':
		userword=None
		try:
			#user=account.models.CustomUser.objects.get(email=request.user)
			#lexicon=Word.objects.filter(belong=slug)#.order_by("word")
			#userlexicon=UserLexicon.objects.filter(user__email=request.user)

			if known==1:  #know this word
				userword=UserWordList.objects.get(user__user__email=request.user,word__word=request.POST.get('word'),word__word__in=Word.objects.filter(belong=slug))	
				userword.is_new=False
				rev_words=UserWordList.objects.filter(user__user__email=request.user,count__gt=0,word__word__in=Word.objects.filter(belong=slug)).count()
				if rev_words==1:
					userword.count=0
				if userword.count>0:
					userword.count-=1
			elif known==0:
				userword=UserWordList.objects.get(user__user__email=request.user,word__word=request.POST.get('word'),word__word__in=Word.objects.filter(belong=slug))	
				userword.is_new=False
				if userword.count<5:
					userword.count+=1
			
			userword.save()
			userword=UserWordList.objects.filter(user__user__email=request.user,is_new=True,word__word__in=Word.objects.filter(belong=slug))	
			
			if userword.count()==0 or int(request.POST.get('times'))%5==0:
				userword=UserWordList.objects.filter(user__user__email=request.user,is_new=False,word__word__in=Word.objects.filter(belong=slug)).order_by('-count')
			
			word=userword[0].word

			
				


		except Lexicon.DoesNotExist:
			raise Http404('Word doesn\'t exist!')

	own_words=UserWordList.objects.filter(user__user__email=request.user)
	total_num=own_words.count()
	new_num=own_words.filter(is_new=True).count()
	rev_num=own_words.filter(count__gt=0).count()
	master_num=own_words.filter(is_new=False,count=0).count()
	rtn_dict={'word':word.word,
					'lexicon':slug,
					'meaning':word.meaning,
					'phonetic':word.phonetic,
					'is_new': 'New',
					'total_num':total_num,
					'new_num':new_num,
					'rev_num':rev_num,
					'master_num':master_num,
					}
	if userword[0].is_new==False:

		del rtn_dict['is_new']
	if request.method=='GET':
		return render(request,'flashcard/card.html',rtn_dict)
	return JsonResponse(rtn_dict)


@csrf_exempt
def take_quiz(request,slug,id):
	#num=8

	if request.method=='GET':
		word=UserWordList.objects.filter(user__user__email=request.user,word__word__in=Word.objects.filter(belong=slug)).order_by('-count')[id].word
		#print(word)
		#print(UserWordList.objects.filter(user__user__email=request.user,word=word))
		wrong_answers=UserWordList.objects.filter(user__user__email=request.user).exclude(word=word).order_by('?').values('word')[:3]
		wrong_answers=Word.objects.filter(word__in=wrong_answers).values('meaning')
		wrong_ans=list(wrong_answers)
		right_idx=random.randint(0,3)
		wrong_ans.insert(right_idx,{'meaning':word.meaning})
		rtn_dict={'word':word.word, \
			'right_idx':right_idx,
			'ans1':wrong_ans[0]["meaning"],
			'ans2':wrong_ans[1]["meaning"],
			'ans3':wrong_ans[2]["meaning"],
			'ans4':wrong_ans[3]["meaning"],
			'lexicon':slug
		}
		if id==0:
			return render(request,'flashcard/quiz.html',rtn_dict)
		return JsonResponse(rtn_dict)
	if request.method=='POST':
		word=UserWordList.objects.filter(user__user__email=request.user,word__word__in=Word.objects.filter(belong=slug)).order_by('-count')[id].word
		userWord=UserWordList.objects.get(user__user__email=request.user,word__belong=slug,word__word=request.POST.get('word'))
		if int(request.POST.get('result')) ==0:
			userWord.count=userWord.count+1
			userWord.save()

		#print(word)
		#print(UserWordList.objects.filter(user__user__email=request.user,word=word))
		wrong_answers=UserWordList.objects.filter(user__user__email=request.user).exclude(word=word).order_by('?').values('word')[:3]
		wrong_answers=Word.objects.filter(word__in=wrong_answers).values('meaning')
		wrong_ans=list(wrong_answers)
		right_idx=random.randint(0,3)
		wrong_ans.insert(right_idx,{'meaning':word.meaning})
		rtn_dict={'word':word.word, \
			'right_idx':right_idx,
			'ans1':wrong_ans[0]["meaning"],
			'ans2':wrong_ans[1]["meaning"],
			'ans3':wrong_ans[2]["meaning"],
			'ans4':wrong_ans[3]["meaning"],
			'lexicon':slug
		}
		if id==0:
			return render(request,'flashcard/quiz.html',rtn_dict)
		return JsonResponse(rtn_dict)




		



'''
# Create your views here.
def UploadWords():
	saved=False
	print(requst.method)
	if request.method=='POST':
		myForm=LexiconForm(request.POST,request.FILES)

		if myForm.is_valid():
			#importWords(request.FILES['file'])
			lexicon = Lexicon()
			lexicon.name = myForm.cleaned_data["name"]
			lexicon.file = myForm.cleaned_data["file"]
			lexicon.save()
			saved = True
	else:
		myForm = LexiconForm()
		
	return render(request, 'base.html',{'form': myForm,'saved':saved})
'''