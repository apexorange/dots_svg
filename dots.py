import random
import xml.etree.ElementTree as ET


def generate_non_overlapping_dots(width, height, num_black, num_red, radius):
    # Prepare to collect dot information
    dots = []
    attempts_per_dot = 100  # Max attempts to place a dot before skipping

    # Function to check if a new dot overlaps with existing dots
    def overlaps(new_x, new_y):
        min_distance = 2 * radius
        for x, y, _ in dots:
            if ((new_x - x) ** 2 + (new_y - y) ** 2) ** 0.5 < min_distance:
                return True
        return False

    # Function to generate dots of a specific color
    def generate_dots(num, color):
        for _ in range(num):
            placed = False
            for _ in range(attempts_per_dot):
                x = random.uniform(radius, width - radius)
                y = random.uniform(radius, height - radius)
                if not overlaps(x, y):
                    dots.append((x, y, color))
                    placed = True
                    break
            if not placed:
                print(f"Could not place a {color} dot after {attempts_per_dot} attempts.")

    # Generate black and red dots
    generate_dots(num_black, '#bfbfbf')
    generate_dots(num_red, 'red')

    return dots


def create_svg(dots, width, height, file_name):
    # Create an SVG element
    svg = ET.Element('svg', width=str(width), height=str(height), xmlns="http://www.w3.org/2000/svg")

    # Add dots to the SVG
    for x, y, color in dots:
        dot = ET.SubElement(svg, 'circle', cx=str(x), cy=str(y), r='5', fill=color)

    # Write to file
    tree = ET.ElementTree(svg)
    tree.write(file_name)

# Example usage:
dots = generate_non_overlapping_dots(1920, 1080, 5000, 50, 5)
create_svg(dots, 1920, 1080, 'dots.svg')
