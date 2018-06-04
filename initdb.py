import xlrd 
import django
import os




def create_lexicon(filename,lexicon_name):
	from card.models import Word
	wb=xlrd.open_workbook(filename=filename)
	table=wb.sheets()[0]
	row=table.nrows
	for i in range(row):
		word=Word(word=table.row_values(i)[0],meaning=table.row_values(i)[1],phonetic=table.row_values(i)[2],belong=lexicon_name)
		word.save()



def main():
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vocabulary.settings")
	django.setup()
	filename='file/lexicon.xlsx'
	lexicon_name='toefl'
	#filename='file/lexicon_gre.xlsx'
	#lexicon_name='gre'
	create_lexicon(filename,lexicon_name)


 
 
if __name__ == '__main__':
	main()
