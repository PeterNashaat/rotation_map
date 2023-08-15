from django.shortcuts import render
from .forms import StationAssignmentForm

def generate_table(request):
    if request.method == 'POST':
        form = StationAssignmentForm(request.POST)
        if form.is_valid():
            num_stations = form.cleaned_data['num_stations']
            num_teams = form.cleaned_data['num_teams']
            station_names = form.cleaned_data['station_names'].split(',')

            # Generate the table data
            stations = ['Station {}'.format(i + 1) for i in range(num_stations)]
            teams = ['Team {}'.format(i + 1) for i in range(num_teams)]

            # Generate assignments for each station with shifting team order
            assignments = []

            for team_idx, team in enumerate(teams):
                team_assignments = [team] + [station_names[(station_idx + team_idx) % num_stations] for station_idx in range(num_stations)]
                assignments.append(team_assignments)

            # First row with station numbers
            first_row = ['St/Te'] + stations
            assignments.insert(0, first_row)

            return render(request, 'table.html', {'assignments': assignments})

    else:
        form = StationAssignmentForm()

    return render(request, 'generate_table.html', {'form': form})

