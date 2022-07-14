# Generated by Django 4.0.6 on 2022-07-13 17:10

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
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('banner', models.ImageField(default='images/genre_banners/default.png', upload_to='images/genre_banners/')),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('banner', models.ImageField(default='images/mood_banners/default.png', upload_to='images/mood_banners/')),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('banner', models.ImageField(default='images/song_banners/default.png', upload_to='images/song_banners/')),
                ('audio_file', models.FileField(upload_to='songs/')),
                ('favourite_by', models.ManyToManyField(blank=True, related_name='favourite_songs', to=settings.AUTH_USER_MODEL)),
                ('genre', models.ManyToManyField(blank=True, related_name='songs', to='songs.genre')),
                ('mood', models.ManyToManyField(blank=True, related_name='songs', to='songs.mood')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='songs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='songs.song')),
            ],
        ),
    ]
