from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.template import Library
from .forms import *
from .models import *
from django.core.files.storage import FileSystemStorage
import xlrd 
from django.views.generic import TemplateView
from django.http import Http404,JsonResponse
from django.shortcuts import render
import account
from django.views.decorators.csrf import csrf_exempt
import random
from django.utils import timezone
from django.db.models import Q,F
import datetime
from django.contrib.auth.decorators import login_required

@login_required
def setPlan(request):
	now = timezone.now()
	print('我')
	if request.method=='POST' and 'plan' in request.POST :
		learn=UserWordList.objects.filter(date_created__lt=F('date_modified'),date_modified__date=datetime.date.today(),user__user=request.user).count()
		userplan=UserPlan.objects.get(user=request.user)
		userplan.amount=request.POST["plan"]
		userplan.save()

		return render(request, 'home.html', {'learn_num':learn,'plan_num':userplan.amount,'saved_plan': 1})
	elif request.method=='GET':
		print(UserWordList.objects.filter(date_created__lt=F('date_modified'),date_modified__date=datetime.date.today(),user__user=request.user))
		learn=UserWordList.objects.filter(date_created__lt=F('date_modified'),date_modified__date=datetime.date.today(),user__user=request.user).count()
		userplan=UserPlan.objects.get(user=request.user)

		return render(request, 'home.html', {'learn_num':learn,'plan_num':userplan.amount,'saved_plan': 0})
	else:
		learn=UserWordList.objects.filter(date_created__lt=F('date_modified'),date_modified__date=datetime.date.today(),user__user=request.user).count()
		userplan=UserPlan.objects.get(user=request.user)
		rtn_dict=addCustomizeWord(request) 
		rtn_dict['learn_num']=learn
		rtn_dict['plan_num']=userplan.amount
		rtn_dict['saved_plan']=0
		return render(request, 'home.html', rtn_dict)


#@login_required
class UploadWordsView(TemplateView):
	template_name = 'card.html'

	def post(self, request, *args, **kwargs):
		context = self.get_context_data()
		saved=False


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

@login_required
def detail(request,slug,known,**kwargs):
	is_new='New'
	if request.method == 'GET':
		userword=UserWordList.objects.filter(user__user=request.user,is_new=True,word__word__in=Word.objects.filter(belong=slug))	
				#userword=userwords.objects.filter(belong=slug)
		if(userword.count()!=0):
			word=userword[0].word
		else:
			userword=UserWordList.objects.filter(user__user=request.user,is_new=False,word__word__in=Word.objects.filter(belong=slug)).order_by('-count')
			word=userword[0].word


	elif request.method == 'POST':
		userword=None
		
		try:
			if known==1:  #know this word
				userword=UserWordList.objects.get(user__user=request.user,word__word=request.POST.get('word'),word__word__in=Word.objects.filter(belong=slug))	
				userword.is_new=False
				rev_words=UserWordList.objects.filter(user__user=request.user,count__gt=0,word__word__in=Word.objects.filter(belong=slug)).count()
				if rev_words==1:  #only 1 word need review
					userword.count=0
				if userword.count>0:  #remeber this word
					userword.count-=1
			elif known==0:
				userword=UserWordList.objects.get(user__user=request.user,word__word=request.POST.get('word'),word__word__in=Word.objects.filter(belong=slug))	
				userword.is_new=False
				if userword.count<5:   #penalty for forget the word
					userword.count+=1
			
			userword.save()
			userword=UserWordList.objects.filter(user__user=request.user,is_new=True,word__word__in=Word.objects.filter(belong=slug))	

			if userword.count()==0 or int(request.POST.get('times'))%5==0:   #The word need review beore today
				word=UserWordList.objects.filter(~Q(date_modified__date=datetime.date.today()),user__user=request.user,is_new=False,word__word__in=Word.objects.filter(belong=slug)).order_by('-count')
				is_new='Review'
				if(word.count()!=0):
					userword=word
			if userword.count()==0 or int(request.POST.get('times'))%3==0:
				word=UserWordList.objects.filter(user__user=request.user,count__gt=0,date_modified__date=datetime.date.today(),word__word__in=Word.objects.filter(belong=slug)).order_by('-count')	#Today's need review
				if(word.count()!=0):
					userword=word
				is_new='Learning'
			if userword.count()==0 or int(request.POST.get('times'))%7==0:
				word=UserWordList.objects.filter(user__user=request.user,count__exact =0,word__word__in=Word.objects.filter(belong=slug))	#Today's need review
				if(word.count()!=0):
					userword=word
				is_new='Mastered'
			if userword.count()==0 or int(request.POST.get('times'))%2==0:
				word=UserWordList.objects.filter(~Q(date_modified__date=datetime.date.today()),user__user=request.user,is_new=False,word__word__in=Word.objects.filter(belong=slug)).order_by('-date_modified')
				if(word.count()!=0):
					userword=word
				is_new='Review'
			if is_new=='Mastered' or is_new=='Learning':
				word=userword[random.randint(0,userword.count()-1)].word
			else:
				word=userword[0].word

		except Lexicon.DoesNotExist:
			raise Http404('Word doesn\'t exist!')

	own_words=UserWordList.objects.filter(user__user=request.user,word__word__in=Word.objects.filter(belong=slug))
	total_num=own_words.count()
	new_num=own_words.filter(is_new=True).count()
	rev_num=own_words.filter(count__gt=0).count()
	master_num=own_words.filter(is_new=False,count=0).count()
	rtn_dict={'word':word.word,
					'lexicon':slug,
					'meaning':word.meaning,
					'phonetic':word.phonetic,
					'is_new': is_new,
					'total_num':total_num,
					'new_num':new_num,
					'rev_num':rev_num,
					'master_num':master_num,
					}

	if request.method=='GET':
		return render(request,'flashcard/card.html',rtn_dict)
	return JsonResponse(rtn_dict)


@csrf_exempt
@login_required
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

@login_required
def deleteCustomizeWord(request,slug):	
	if request.method=='POST':
		try:
			word=Word.objects.get(word=slug,belong=request.user)
			word.delete()
		except:
			user_word=CustomizedLexicon.objects.get(word__word = slug)
			user_word.delete()
		rtn_dict={
		'info':"Delete Successfully!"
		}
		return JsonResponse(rtn_dict)


@login_required
def addCustomizeWord(request):

	rtn_dict={}
	if request.method=='POST' and 'new_word' in request.POST:
		form=CustomizedWordForm(request.POST)
		if form.is_valid():

			try:
				word=Word.objects.get(word=request.POST['new_word'],belong=request.user.email)
				rtn_dict['saved']= 0
			except:
				word=Word(word=form.cleaned_data["new_word"],meaning=form.cleaned_data["new_meaning"],phonetic=form.cleaned_data["new_phonetic"],belong=request.user.email)
				word.save()
				user=request.user
				custom=CustomizedLexicon(user=user,word=word)
				custom.save()
				rtn_dict['saved']= 1

		
		
	else:
		form = CustomizedWordForm()
	rtn_dict['form']=form
	#return render(request, 'home.html', {'form': form,'saved': 2})
	return rtn_dict


@login_required
def listCustomizeWord(request):
	
	if request.method=='GET':
		all_words=CustomizedLexicon.objects.filter(user__email=request.user)
		return render(request, 'flashcard/user_words.html', {'words':all_words})



		



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