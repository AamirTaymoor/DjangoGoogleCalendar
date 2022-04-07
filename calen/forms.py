from django  import forms


class CreateEvent(forms.Form):
    cal_id = forms.CharField(max_length=100, label="calendar id")
    attendee= forms.CharField(max_length= 500,label='add attendees seperated by comma')
    summary = forms.CharField(max_length=100, label='summary')

class DeleteEvent(forms.Form):
    cal_id = forms.CharField(max_length=100, label='Enter Calendar Id')
    event_id = forms.CharField(max_length=100, label='Event id')
    
class UpdateEvent(forms.Form):
    cal_id = forms.CharField(max_length=100, label='Enter Calendar Id')
    event_id = forms.CharField(max_length=100, label='Event id')
    summary = forms.CharField(max_length=500, label='summary to be updated')