

# = Cosmos Population =========================================================
"""
"""


# - Dependencies ---------------------------------
# Python Modules
import os
import csv
import math
from random import random
# Local Modules
from config import *
from vector3d import *
from particle import Particle


# - Program Constants ----------------------------
dir_path = os.path.dirname(os.path.realpath(__file__))


# - Star Population from File --------------------
def populate_stars():
    with open(F'{dir_path}/stars.csv', 'r', newline='') as csv_file:
        line_reader = csv.reader(csv_file)
        # The Bayer / Flamsteed
        # absolute_magnitude,
        # right_ascension,
        # declination,
        # distance,
        # label,
        count = 0
        stars = []
        for row in line_reader:
            right_ascension = float(row[2])
            declination = float(row[3])
            distance = float(row[4])
            absolute_magnitude = float(row[1])
            label = row[5]
            star_z = math.sin(right_ascension+RIGHT) * math.cos(declination)
            star_x = math.cos(right_ascension+RIGHT) * math.cos(declination)
            star_y = math.sin(declination)
            star_position = (-star_x, star_y, star_z)
            star_position = scale_vector(star_position, distance)
            new_star = Particle(
                star_position,
                random()*695000*MEGA,
                magnitude=absolute_magnitude,
            )
            if label:
                new_star.label = label
            stars.append(new_star)
        return stars


def translate():
    stars = []
    with open('hygfull.csv', newline='') as csv_file:
        line_reader = csv.reader(csv_file)
        print(line_reader.__next__())  # Skip first line
        # The Bayer / Flamsteed: 5
        # Right Ascension, Declination: 7, 8
        # distance: 9
        # Apparent Magnitude: 10
        # Absolute Magnitude: 11
        count = 0
        for row in line_reader:
            try:
                if(float(row[10]) > 5):  # Apparent Magnitude
                    continue
            except ValueError:
                continue
            right_ascension = float(row[7]) * (math.pi/12)  # Hours to radians
            declination = float(row[8]) * (math.pi/180)  # Degrees to radians
            distance = float(row[9]) * PARSEC
            absolute_magnitude = float(row[11])
            stars.append([
                row[5],
                absolute_magnitude,
                right_ascension,
                declination,
                distance,
                '',
            ])
    with open('stars.csv', 'w', newline='') as csv_file:
        line_writer = csv.writer(csv_file)
        for row in stars:
            line_writer.writerow(row)
