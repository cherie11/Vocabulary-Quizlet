
from card.models import Word,UserWordList
    
def initUserLexicon(account):
    import sys
    sys.path.append("..")
    querysetlist=[]
    wordlist=Word.objects.all()
    print(wordlist)
    for word in wordlist:
    	querysetlist.append(UserWordList(user=account,word=word))
    UserWordList.objects.bulk_create(querysetlist)


