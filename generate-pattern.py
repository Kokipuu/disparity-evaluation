import matplotlib.pyplot as plt
import numpy as np

def generate_random_circle(radius, x_range, y_range):
    center_x = np.random.uniform(radius, x_range - radius)
    center_y = np.random.uniform(radius, y_range - radius)
    return center_x, center_y

def circles_do_not_overlap(circles, new_circle, min_distance):
    for circle in circles:
        distance = np.sqrt((circle[0] - new_circle[0]) ** 2 + (circle[1] - new_circle[1]) ** 2)
        if distance < min_distance:
            return False
    return True

def generate_random_non_overlapping_circles(num_circles, radius, x_range, y_range, min_distance):
    circles = []
    for _ in range(num_circles):
        while True:
            new_circle = generate_random_circle(radius, x_range, y_range)
            if circles_do_not_overlap(circles, new_circle, min_distance):
                circles.append(new_circle)
                break
    return circles

def plot_circles_in_rectangle(circles, rectangle_width, rectangle_height):
    fig, ax = plt.subplots()
    ax.set_xlim(0, rectangle_width)
    ax.set_ylim(0, rectangle_height)
    for circle in circles:
        circle_patch = plt.Circle(circle, radius, color='b', fill=False)
        ax.add_patch(circle_patch)
    ax.set_aspect('equal', 'box')
    plt.show()

rectangle_width = 10
rectangle_height = 8
num_circles = 100
radius = 0.3
min_distance = 2 * radius

circles = generate_random_non_overlapping_circles(num_circles, radius, rectangle_width, rectangle_height, min_distance)
plot_circles_in_rectangle(circles, rectangle_width, rectangle_height)





# import cv2 as cv
# import matplotlib.pyplot as plt
# import numpy as np
# from matplotlib.patches import Circle, Rectangle as MatplotlibRectangle, RegularPolygon
# from matplotlib.transforms import Affine2D



# class Rectangle:

#     def __init__(self, width, height):
#         self.width = width
#         self.height = height
#         self.shapes = []

#     def add_shape(self, shape_type, size, position):
#         if shape_type == "circle":
#             self.shapes.append({"type": "circle", "size": size, "position": position})
#         elif shape_type == "triangle":
#             self.shapes.append({"type": "triangle", "size": size, "position": position})
#         elif shape_type == "rectangle":
#             self.shapes.append({"type": "rectangle", "size": size, "position": position})
#         else:
#             print("Unsupported shape type")

#     def draw(self):
#         fig, ax = plt.subplots(figsize=(21, 29.7), dpi=100)
#         ax.set_xlim(0, self.width)
#         ax.set_ylim(0, self.height)
#         ax.axis("off")

#         for shape in self.shapes:
#             shape_type = shape["type"]
#             size = shape["size"]
#             position = shape["position"]

#             if shape_type == "circle":
#                 circle = Circle(position, size, color="black")
#                 ax.add_patch(circle)
#             elif shape_type == "triangle":
#                 triangle = RegularPolygon(position, numVertices=3, radius=size, color="black")
#                 rotation = Affine2D().rotate_deg(30)
#                 triangle.set_transform(rotation + ax.transData)
#                 ax.set_xlim(center[0] - size - 1, center[0] + size + 1)
#                 ax.set_ylim(center[1] - size - 1, center[1] + size + 1)
#                 ax.add_patch(triangle)
#             elif shape_type == "rectangle":
#                 angle = np.random.uniform(0, 90)  # if angle is to 0, rectangle does't rotate. 
#                 # angle = 0
#                 rect = MatplotlibRectangle((position[0] - size[0]/2, position[1] - size[1]/2), size[0], size[1], angle = angle, color="black")
#                 ax.add_patch(rect)

#         plt.gca().set_aspect('equal', adjustable='box')
#         plt.savefig('pattern/rotation.png')
#         plt.show()




# def generate_random_point(x_range, y_range, seed):
#     x = np.random.uniform(0, x_range)
#     y = np.random.uniform(0, y_range)
#     return x, y


# def genareta_radom_size(size, shape_type, seed):
#     if shape_type == "circle":
#         s = np.random.uniform(0, size)
#         return s
#     elif shape_type == "triangle":
#         s = np.random.uniform(0, size)
#         return s
#     elif shape_type == "rectangle":
#         s_width = np.random.uniform(0, size)
#         s_height = np.random.uniform(0, size)
#         return s_width, s_height
#     else:
#         return "Unsupported shape type"




# if __name__ == '__main__':
#     WIDTH, HEIGHT = 21, 29
#     X_RANGE, Y_RANGE = 21, 29
#     SEED = 10
#     NUM = 500
#     SIZE = 0.3
#     SHAPE_TYPE = "rectangle"

#     np.random.seed(SEED)


#     # Create a rectangle object
#     main_rectangle = Rectangle(width=WIDTH, height=HEIGHT)

#     for _ in range(NUM):
#         x, y = generate_random_point(X_RANGE, Y_RANGE, SEED)

#         if SHAPE_TYPE == "circle":
#             # s = genareta_radom_size(SIZE, SHAPE_TYPE, SEED)
#             # Add shapes to the rectangle
#             # main_rectangle.add_shape(shape_type="circle", size=s, position=(x, y))
#             main_rectangle.add_shape(shape_type="circle", size=SIZE, position=(x, y))

#         elif SHAPE_TYPE == "triangle":
#             # s = genareta_radom_size(SIZE, SHAPE_TYPE, SEED)
#             # Add shapes to the rectangle
#             # main_rectangle.add_shape(shape_type="triangle", size=1.5, position=(x, y))
#             main_rectangle.add_shape(shape_type="triangle", size=SIZE, position=(x, y))

#         elif SHAPE_TYPE == "rectangle":
#             # s_width, s_height = genareta_radom_size(SIZE, SHAPE_TYPE, SEED)
#             # Add shapes to the rectangle
#             # main_rectangle.add_shape(shape_type="rectangle", size=(2, 1), position=(x, y))
#             main_rectangle.add_shape(shape_type="rectangle", size=(SIZE, SIZE), position=(x, y))


#     # Draw the rectangle with the shapes
#     img = main_rectangle.draw()
    
