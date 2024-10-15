from datetime import datetime,date,timedelta
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Count


class Command(BaseCommand):

    help='Добавление поездов в расписание'

    def add_arguments(self,parser):
        parser.add_argument('--days', dest='days', type=int)

    def handle(self, *args,**options):
        times=[('07','00','00'),('17','00','00')]
        subject='Add trains'
        date_joined=date.today()+timedelta(days=options['days'])
        trains=Trains.objects.all()
        for train in trains:
            for t in times:
                tr=ScheduleTrians(train=train, date_train=date.today()+timedelta(days=options['days']),
                                time_train=time(t[0],t[1],t[2]))
                tr.save()

            
