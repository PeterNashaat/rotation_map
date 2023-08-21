import random
from django.shortcuts import render
from django.http import HttpResponse
from io import BytesIO
import matplotlib.pyplot as plt
from .forms import StationAssignmentForm
from PIL import Image

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

            # Define color options
            color_options = ['023e8a', '0077b6', '0096c7', '00b4d8', '48cae4', '90e0ef', 'ade8f4', 'caf0f8']

            # Assign random colors to each row
            assignments_with_colors = []
            for row in assignments:
                color = random.choice(color_options)
                assignments_with_colors.append({'assignments': row, 'color': color})

            return render(request, 'table.html', {'assignments_with_colors': assignments_with_colors})

    else:
        form = StationAssignmentForm()

    return render(request, 'generate_table.html', {'form': form})

def generate_table_image(request):
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

            # First row with station numbers and team names
            first_row = ['St/Te'] + stations
            assignments.insert(0, first_row)

            # Define color options
            color_options = ['023e8a', '0077b6', '0096c7', '00b4d8', '48cae4', '90e0ef', 'ade8f4', 'caf0f8']

            # Assign random colors to each row
            assignments_with_colors = []
            for row in assignments:
                color = random.choice(color_options)
                color_row = ['#{}'.format(color)] * len(row)
                assignments_with_colors.append({'assignments': row, 'color_row': color_row})

            # Generate an image with larger dimensions
            plt.figure(figsize=(12, 8))
            plt.axis('off')

            # Create a list of colors for each row
            cell_colors = [row['color_row'] for row in assignments_with_colors]

            plt.table(cellText=[row['assignments'] for row in assignments_with_colors], cellLoc='center', colLabels=None, cellColours=cell_colors, loc='center')
            buffer = BytesIO()
            plt.savefig(buffer, format="jpg", bbox_inches='tight', dpi=300)  # Save as JPEG
            plt.close()
            buffer.seek(0)

            # Convert the image to JPEG format using PIL
            pil_image = Image.open(buffer)
            jpg_image = BytesIO()
            pil_image.save(jpg_image, format="JPEG")
            jpg_image.seek(0)

            response = HttpResponse(jpg_image.getvalue(), content_type="image/jpeg")
            response['Content-Disposition'] = 'attachment; filename=table_image.jpg'
            return response
    else:
        form = StationAssignmentForm()

    return render(request, 'generate_table.html', {'form': form})

    return HttpResponse(status=400)  # Bad request if form is not valid
