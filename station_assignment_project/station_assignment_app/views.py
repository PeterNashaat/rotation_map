import random
from django.shortcuts import render
from django.http import HttpResponse
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
from .forms import StationAssignmentForm
import numpy as np

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
            color_options = ['c9184a', 'b8c0ff', 'ccd5ae', 'ffb4a2', 'f8ad9d', '90e0ef', 'ade8f4', 'caf0f8', 'd0fffa', '678c95', '46d0d0', 'f9f2e0', '7da97a', 'd5bdaf', '84a59d', 'f28482', '4cc9f0', 'ffdab9', '57cc99', 'fb6f92']

            # Shuffle the color options to randomize them
            random.shuffle(color_options)

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
            color_options = ['c9184a', 'b8c0ff', 'ccd5ae', 'ffb4a2', 'f8ad9d', '90e0ef', 'ade8f4', 'caf0f8', 'd0fffa', '678c95', '46d0d0', 'f9f2e0', '7da97a', 'd5bdaf', '84a59d', 'f28482', '4cc9f0', 'ffdab9', '57cc99', 'fb6f92']

            # Shuffle the color options to randomize them
            random.shuffle(color_options)

            # Assign colors to each row
            assignments_with_colors = []
            for row in assignments:
                color = color_options.pop(0)  # Get the first color and remove it from the list
                color_row = ['#{}'.format(color)] * len(row)
                assignments_with_colors.append({'assignments': row, 'color_row': color_row})

            # Calculate the size of the figure to fit the table
            num_rows = len(assignments_with_colors)
            num_columns = len(assignments_with_colors[0]['assignments'])
            table_width = 7  # Adjust this value as needed to control the table width
            table_height = 1 * num_rows / num_columns  # Adjust this value to control the table height

            # Generate an image with the calculated dimensions
            plt.figure(figsize=(table_width, table_height))
            plt.axis('off')

            # Create a list of colors for each row
            cell_colors = [row['color_row'] for row in assignments_with_colors]

            # Increase font size for the table
            table = plt.table(cellText=[row['assignments'] for row in assignments_with_colors], cellLoc='center', colLabels=None, cellColours=cell_colors, loc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(7)  # Adjust the font size as needed

            buffer = BytesIO()
            plt.savefig(buffer, format="jpg", bbox_inches='tight', dpi=1000)  # Save as JPEG
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
