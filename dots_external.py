import random
import xml.etree.ElementTree as ET


def generate_dots(width, height, num_black, num_red, radius, scale, allow_overlap=True):
    # Prepare to collect dot information
    dots = []
    attempts_per_dot = 100  # Max attempts to place a dot before skipping
    adjusted_radius = radius * scale  # Adjust radius based on scale

    # Function to check if a new dot overlaps with existing dots
    def overlaps(new_x, new_y):
        min_distance = 2 * adjusted_radius
        for x, y, _ in dots:
            if ((new_x - x) ** 2 + (new_y - y) ** 2) ** 0.5 < min_distance:
                return True
        return False

    # Function to generate dots of a specific color
    def generate_dots(num, color):
        for _ in range(num):
            placed = False
            for _ in range(attempts_per_dot):
                x = random.uniform(adjusted_radius, width - adjusted_radius)
                y = random.uniform(adjusted_radius, height - adjusted_radius)
                if allow_overlap or not overlaps(x, y):
                    dots.append((x, y, color))
                    placed = True
                    break
            if not placed and not allow_overlap:
                print(f"Could not place a {color} dot after {attempts_per_dot} attempts.")

    # Generate black and red dots
    generate_dots(num_black, 'black')
    generate_dots(num_red, 'red')

    return dots


def create_svg(dots, width, height, file_name, shape_content, scale, radius):
    # Create an SVG element
    svg = ET.Element('svg', width=str(width), height=str(height), xmlns="http://www.w3.org/2000/svg",
                     xmlns_xlink="http://www.w3.org/1999/xlink")

    # Define shapes using defs with the content from shape.svg
    defs = ET.SubElement(svg, 'defs')
    shape = ET.SubElement(defs, 'path', id='externalShape', d=shape_content)

    # Add referenced shapes to the SVG using <use> with scale transformation
    for x, y, color in dots:
        use_shape = ET.SubElement(svg, 'use', href='#externalShape', x=str(x), y=str(y), fill=color)
        # Translate the shape to align properly based on its original center (assumed center here)
        use_shape.set('transform', f'translate({-radius * scale} {-radius * scale}) scale({scale})')

    # Write to file
    tree = ET.ElementTree(svg)
    tree.write(file_name)

# Example usage (assuming you have the actual path content and desired scale):
shape_content = 'M10 10 H 90 V 90 H 10 L 10 10'  # Replace with actual content from shape.svg
radius = 10
scale = 1  # Example scaling factor to increase the size by 50%
dots = generate_dots(1920, 1080, 950, 50, radius, scale, allow_overlap=False)
create_svg(dots, 1920, 1080, 'dots_with_shapes.svg', shape_content, scale, radius)
