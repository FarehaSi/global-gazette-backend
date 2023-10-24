# Generated by Django 4.2.6 on 2023-10-24 00:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_reaction_remove_like_article_remove_like_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='articles.comment'),
        ),
        migrations.AddField(
            model_name='reaction',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_reactions', to='articles.comment'),
        ),
        migrations.AlterField(
            model_name='reaction',
            name='article',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article_reactions', to='articles.article'),
        ),
    ]
