# Documentation For Coding A  Game In Tyro Engine

## Object

### Image

- Attributes
  - x - x coordinate of the image
  - y - y coordinate of the image
  - scale - Scale of the image
  - width  - Width of the image 
  - height  - Height of the image
- Methods
  - move_x - Move the x position of the image
  - move_y - Move the y position of the image
  - change_Width - Change width of the image
  - change_Height - Change height of the image
  - change_Scale - Change scale of the image
  - goto - Go to `x, y` position

### Rectangle / Ellipse

- Attributes
  - x - x coordinate of the object
  - y - y coordinate of the object
  - scale - Scale of the object
  - width  - Width of the object
  - height  - Height of the object
  - color - Color of the object
- Methods
  - move_x - Move the x position of the object
  - move_y - Move the y position of the object
  - change_Width - Change width of the object
  - change_Height - Change height of the object
  - change_Scale - Change scale of the object
  - change_Color- Change color of the object
  - goto - Go to `x, y` position

### Line

- Attributes
  - x - x coordinate of the object
  - y - y coordinate of the object
  - scale - Scale of the object
  - width - Width of the object
  - height - Height of the object
  - color - Color of the object
  - thickness - Color of the object
- Methods
  - move_x - Move the x position of the object
  - move_y - Move the y position of the object
  - change_Width - Change width of the object
  - change_Height - Change height of the object
  - change_Scale - Change scale of the object
  - change_Color- Change color of the object
  - change_Thickness - Change thickness of the object
  - goto - Go to `x, y` position

###  Text

- Attributes
  - x - x coordinate of the text
  - y - y coordinate of the text
  - color - Color of the text
  - font - Font of the text
  - size - Size of the text
  - text - Text of the text
- Methods
  - move_x - Move the x position of the object
  - move_y - Move the y position of the object
  - change_Color- Change color of the object
  - change_Text - Change text of the text
  - goto - Go to `x, y` position

## In-Built

- Attributes
  - init - True for the first frame, used for initializing variables etc
- Methods
  - random -  takes two integers and returns a random value between them
  - delay - sleeps for `x` seconds
  - isColliding - takes two objects and returns weather they are colliding or not
  - isKey - takes a key and returns weather the key is pressed or not
  - mousePos - returns a list with x and y coordinates of the cursor 

