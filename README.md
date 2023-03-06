# 3DGraphicsOn2D

The code does not use any 3D-graphics package or 3D-graphics library.
This has been attempted in Python3 on Jupyter Notebook Environment.

I have used the pygame library (2D-graphics library) to display the graphics. Thus, it must be installed for the code to run. Comments have been added all through the code for easy understanding.

The coordinate frame of the window has been set such that:

•	the positive X-axis is pointing horizontally to the right,

•	the positive Y-axis is pointing vertically upward,

•	the positive Z-axis is pointing out of the plane of the window toward the observer,

•	the origin is at the center of the window.

# Code explanation for wireframe.py:


I have first defined the colours to be used in the display of graphics followed by window size and center. Further, pygame has been initialized and I set up the display.

First function is for reading the object from the file and another one is for drawing the object where the edges have been drawn along with the vertices with blue color.

Another function defined after the above two is Center-object where I get the average x, y, and z values of all vertices, subtract the average values from each vertex to center the object around the origin.


In the Main function, the following takes place:

  The object is centered around the origin and later scaled to fit the screen.
  
  An event loop has been set up where the mouse functionalities have been added as asked. First, I rotate object if mouse is being dragged. For this, I calculate horizontal and vertical mouse movement, rotation angles and then rotate the object about X and Y axes using 2 new functions. At last, the previous mouse position is updated. The screen is cleared for the object to be drawn and the display to be continuously updated while controlling the frame rate.
  
The function for rotating about y-axis includes getting the center of the object, creating rotation matrix, translating object to the origin, rotate object about Y axis, and translating object back to its original position.

The function for rotating about x-axis includes getting the center of the object, creating rotation matrix, translating object to the origin, rotating object about X axis and translating object back to its original position.


In faces.py, only one function has been modified:

Draw-object. Here I have added 4 things:

        1 Compute face normal
        
        2 Compute angle with Z-axis
        
        3 Interpolate color between #00005F and #0000FF based on angle
        
        4 Draw face with interpolated color

