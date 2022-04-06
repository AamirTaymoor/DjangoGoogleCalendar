from __future__ import print_function
from ast import Del
from time import strftime

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from httplib2 import Http
from .forms import CreateEvent, DeleteEvent, UpdateEvent
import requests
import os
import json
from . models import CalList, EventList
import datetime
import os.path


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            '/home/aamir/Desktop/projects/django-blog/g_calen/GCalendar/credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
                token.write(creds.to_json())

service = build('calendar', 'v3', credentials=creds)

def Home(request):
    return render(request, 'calen/home.html')


class Authenticate(View):
    def get(self, request):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    '/home/aamir/Desktop/projects/django-blog/g_calen/GCalendar/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('calendar', 'v3', credentials=creds)

            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            print('Getting the upcoming 10 events')
            events_result = service.events().list(calendarId='primary', timeMin=now,
                                                maxResults=10, singleEvents=True,
                                                orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                print('No upcoming events found.')
                return HttpResponse('No upcoming events found.')

            # Prints the start and name of the next 10 events
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                #print(start, event['summary'])
                return HttpResponse(start, event['summary'])

        except HttpError as error:
            #print('An error occurred: %s' % error)
            return HttpResponse("An error occured: " + error)

class Calendars(View):
    def get(self, request):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        service = build('calendar', 'v3', credentials=creds)
        calendar = service.calendars().get(calendarId='primary').execute()
        
        #print(calendar_list_entry['summary'])


        return HttpResponse(str(calendar))

class CalendarList(View):
    def get(self, request):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        service = build('calendar', 'v3', credentials=creds)
        cal_list = service.calendarList().list().execute()
        cal_list2 = cal_list['items']
        #print(cal_list2)
        for i in range(len(cal_list2)):
            obj,created1 = CalList.objects.get_or_create(c_id = cal_list2[i]['id'])
            if created1 == True:
                #c = cal_list2[i]['etag']
                #c = c.strip("\'")
                #c = int(c.strip('\"'))
                #print(c)
                obj.etag = cal_list2[i]['etag']
                obj.c_id = cal_list2[i]['id']
                obj.summary= cal_list2[i]['summary']
                #obj.description= cal_list2[i]['description']
                obj.timezone= cal_list2[i]['timeZone']
                obj.accessrole= cal_list2[i]['accessRole']
                obj.save()

        return render(request,'calen/calList.html',{'c_list':CalList.objects.all()})

class EvList(View):
    def get(self, request):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        service = build('calendar', 'v3', credentials=creds)
        ev_list = service.events().list(calendarId='primary').execute()
        ev_list2 = ev_list['items']
        for i in range(len(ev_list2)):
            obj,created1 = EventList.objects.get_or_create(ev_id = ev_list2[i]['id'])
            if created1 == True:
                obj.ev_id = ev_list2[i]['id']
                obj.etag = ev_list2[i]['etag']
                obj.creator= ev_list2[i]['creator']
                obj.start_time= ev_list2[i]['start']
                obj.end_time= ev_list2[i]['end']
                obj.event_link= ev_list2[i]['htmlLink']
                obj.save()

        
        return render(request,'calen/event.html',{'eventlist':EventList.objects.all()})

class CreateEv(View):
    def get(self, request):
        form = CreateEvent()
        return render(request, 'calen/create_event.html', {'form':form})

    def post(self, request):
        form = CreateEvent(request.POST)
        if form.is_valid():
            cal_id = str(form.cleaned_data['cal_id'])
            attendee = str(form.cleaned_data['attendee'])
            summary = str(form.cleaned_data['summary'])
            #print(cal_id, attendee, summary)
        attendees = list(attendee.split(','))
        att = []
        for i in range(len(attendees)):
            item = {'email':attendees[i]}
            att.append(item)
        start_time = datetime.datetime.now()
        s_time = start_time.isoformat('T')
        end_time = datetime.datetime.now() + datetime.timedelta(hours=1)
        e_time = end_time.isoformat('T')
        
        event_body= {
            'summary':summary,
            'start':{'dateTime':s_time,
                    'timeZone':'Asia/Kolkata'},
            'end':{'dateTime':e_time,
                 'timeZone':'Asia/Kolkata'},
            'attendees': att
        }
        print(event_body)
        event = service.events().insert(calendarId=cal_id,sendNotifications=True,sendUpdates='all', body=event_body).execute()
        html_link = event.get('htmlLink')
        return render(request, 'calen/succ_event_page.html', {'link':html_link})
        #return HttpResponse('event created successfully')

class DelEvent(View):
    def get(self, request):
        form = DeleteEvent()
        return render(request, 'calen/del_event.html', {'form':form})
    
    def post(self, request):
        form = DeleteEvent(request.POST)
        if form.is_valid():
            cal_id = form.cleaned_data['cal_id']
            event_id = form.cleaned_data['event_id']

        try:
            devent = service.events().delete(calendarId=cal_id, eventId=event_id).execute()
            instance = EventList.objects.get(ev_id=event_id)
            return render(request, 'calen/succ_del_event.html')
        except Exception as e:
            return HttpResponse("Event does not exist")
        
class UpdEvent(View):
    def get(self, request):
        form = UpdateEvent()
        return render(request, 'calen/upd_event.html', {'form':form})
    
    def post(self, request):
        form = UpdateEvent(request.POST)
        if form.is_valid():
            cal_id = form.cleaned_data['cal_id']
            event_id = form.cleaned_data['event_id']
            summary = form.cleaned_data['summary']
        try:
            ev = service.events().get(calendarId=cal_id, eventId=event_id).execute()
            ev['summary'] = summary
            upd_event = service.events().update(calendarId='primary', eventId=ev['id'], body=ev).execute()

            #instance = EventList.objects.get(ev_id=event_id)
            #instance.summary=upd_event['summary']
            return render(request, 'calen/succ_upd_event.html', {'updated_event':str(upd_event)})
        except Exception as e:
            return HttpResponse("Event does not exist")
    

