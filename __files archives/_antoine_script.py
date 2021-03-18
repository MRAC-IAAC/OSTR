import cv2
import matplotlib.pyplot as plt

# Image path
image_path = 'patterns/01.jpg'
# Image grayscale
image_grayscale = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
# Image binary
image = cv2.threshold(image_grayscale, 128, 255, cv2.THRESH_BINARY)[1]
# Image size
image_width, image_height = image.shape
# Show the image
plt.imshow(image)
plt.show()

neighbours = [-1, 0, 1]
values_found = []

def give_instructions(movement):
    movement_total = abs(movement[0]) + abs(movement[1])
    if movement_total == 1:
        # Orthogonal
        if movement[0] == -1:
            print('go left')
        elif movement[0] == 1:
            print('go right')
        if movement[1] == -1:
            print('go backward')
        elif movement[1] == 1:
            print('go forward')
    else:
        # Oblique
        pass


def calculate_movement(position_from, position_to):
    movement_x = position_from[0] - position_to[0]
    movement_y = position_from[1] - position_to[1]
    movement = [movement_x, movement_y]
    give_instructions(movement)


def find_neighbour(coordinates):
    values_found.append(coordinates)
    for neighbour_x in neighbours:
        for neighbour_y in neighbours:
            neighbour_x_pos = coordinates[0] + neighbour_x
            neighbour_y_pos = coordinates[1] + neighbour_y
            neighbour_coordinates = [neighbour_x_pos, neighbour_y_pos]
            if image[neighbour_x_pos, neighbour_y_pos] == 0 and neighbour_coordinates not in values_found:
                calculate_movement(coordinates, neighbour_coordinates)


for position_x in range(image_width):
    for position_y in range(image_height):
        position_value = image[position_x, position_y]
        if position_value == 0:
            coordinate = [position_x, position_y]
            find_neighbour(coordinate)



