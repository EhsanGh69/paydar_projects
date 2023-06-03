# Generated by Django 4.2.1 on 2023-05-18 10:21

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cheques_receive_pay', '0001_initial'),
        ('non_government_accounts', '0009_alter_partners_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyersSellers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buyer_seller', models.CharField(choices=[('buy', 'خریدار'), ('sel', 'فروشنده')], max_length=3, verbose_name='خریدار / فروشنده')),
                ('full_name', models.CharField(max_length=250, verbose_name='نام و نام خانوادگی')),
                ('phone', models.CharField(max_length=20, verbose_name='شماره تماس')),
                ('address', models.TextField(verbose_name='آدرس')),
                ('contract_image', models.ImageField(upload_to='images/buyers_sellers', verbose_name='تصویر قرارداد')),
                ('payment_order', models.CharField(choices=[('csh', 'نقدی'), ('chq', 'چک'), ('del', 'حین تحویل'), ('dtr', 'انتقال سند')], max_length=3, verbose_name='ترتیب پرداخت')),
                ('cash_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ پرداخت نقدی')),
                ('cash_amount', models.PositiveBigIntegerField(default=0, verbose_name='مبلغ پرداخت نقدی')),
                ('delivery_amount', models.PositiveBigIntegerField(default=0, verbose_name='مبلغ پرداخت حین تحویل')),
                ('doc_transfer_amount', models.PositiveBigIntegerField(default=0, verbose_name='مبلغ پرداخت انتقال سند')),
                ('cheque_payment', models.ForeignKey(help_text='شماره چک مورد نظر را انتخاب کنید', on_delete=django.db.models.deletion.CASCADE, related_name='cheque_payments', to='cheques_receive_pay.cheques', verbose_name='پرداخت به صورت چک')),
                ('delivery_cheque', models.ForeignKey(help_text='شماره چک مورد نظر را انتخاب کنید', on_delete=django.db.models.deletion.CASCADE, related_name='cheque_deliveries', to='cheques_receive_pay.cheques', verbose_name='پرداخت حین تحویل به صورت چک')),
                ('doc_transfer_cheque', models.ForeignKey(help_text='شماره چک مورد نظر را انتخاب کنید', on_delete=django.db.models.deletion.CASCADE, related_name='cheque_doc_transfers', to='cheques_receive_pay.cheques', verbose_name='پرداخت انتقال سند به صورت چک')),
            ],
            options={
                'verbose_name': 'خریدار / فروشنده',
                'verbose_name_plural': 'خریداران / فروشندگان',
            },
        ),
    ]