from django.shortcuts import render
from .forms import StationAssignmentForm

def generate_table(request):
    if request.method == 'POST':
        form = StationAssignmentForm(request.POST)
        if form.is_valid():
            num_stations = form.cleaned_data['num_stations']
            num_teams = form.cleaned_data['num_teams']

            # Generate the table data
            stations = ['Station {}'.format(i + 1) for i in range(num_stations)]
            teams = ['Team {}'.format(i + 1) for i in range(num_teams)]

            # Create assignments with cycling through stations for each team
            assignments = []

            for team_idx in range(num_teams):
                team_assignments = [teams[team_idx]]
                for station_idx in range(num_stations):
                    station = stations[(station_idx + team_idx) % num_stations]
                    team_assignments.append(station)
                assignments.append(team_assignments)

            # First row (header)
            first_row = ['St/Te'] + stations
            assignments.insert(0, first_row)

            return render(request, 'table.html', {'assignments': assignments})

    else:
        form = StationAssignmentForm()

    return render(request, 'generate_table.html', {'form': form})

