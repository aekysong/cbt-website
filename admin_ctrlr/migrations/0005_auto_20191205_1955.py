# Generated by Django 2.0.13 on 2019-12-05 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_ctrlr', '0004_auto_20191202_2027'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentAns',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qtype', models.CharField(choices=[('NA', 'narrative'), ('MC', 'multi_choices')], default='NA', max_length=20)),
                ('qna_ans', models.CharField(max_length=200, null=True)),
                ('qmc_ans', models.CharField(choices=[('ONE', 'choice_one'), ('TWO', 'choice_two'), ('THR', 'choice_three'), ('FOU', 'choice_four'), ('FIV', 'choice_five')], default='ONE', max_length=20)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_ctrlr.Test')),
            ],
        ),
        migrations.RemoveField(
            model_name='questionmc',
            name='std_ans',
        ),
        migrations.RemoveField(
            model_name='questionna',
            name='std_ans',
        ),
    ]