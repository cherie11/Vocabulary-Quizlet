# Generated by Django 2.0 on 2018-04-29 07:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomizedLexicon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custword', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lexicon',
            fields=[
                ('name', models.CharField(default='anonomous', max_length=200, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserLexicon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='UserWordList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lexicon_name', models.CharField(default='Unknown', max_length=200)),
                ('is_new', models.BooleanField(default=True)),
                ('count', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='card.UserLexicon')),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('word', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='单词')),
                ('meaning', models.CharField(max_length=200, verbose_name='释义')),
                ('phonetic', models.CharField(max_length=100, verbose_name='音标')),
                ('belong', models.CharField(max_length=100, verbose_name='所属词典')),
            ],
        ),
        migrations.AddField(
            model_name='userwordlist',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='card.Word'),
        ),
        migrations.AddField(
            model_name='userlexicon',
            name='lexicon',
            field=models.ManyToManyField(through='card.UserWordList', to='card.Word'),
        ),
        migrations.AddField(
            model_name='userlexicon',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userword', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lexicon',
            name='words',
            field=models.ManyToManyField(related_name='lexicon', to='card.Word'),
        ),
        migrations.AddField(
            model_name='customizedlexicon',
            name='words',
            field=models.ManyToManyField(related_name='words', to='card.Word'),
        ),
    ]
