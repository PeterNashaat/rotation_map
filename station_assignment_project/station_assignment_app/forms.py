from django import forms

class StationAssignmentForm(forms.Form):
    num_stations = forms.IntegerField(label='Number of Stations')
    num_teams = forms.IntegerField(label='Number of Teams')
