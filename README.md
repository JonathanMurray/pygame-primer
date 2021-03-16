# Pygame primer

or _"learning Pygame the hard way"_

## 1. Getting started

This chapter is mainly geared toward readers with little or no experience with Pygame and/or software development in
general. More experienced readers may want to skip ahead to later chapters.

### 1.1 Installing Pygame

To be able to use Pygame, you first have to install it. Like most any other Python packages, it can be installed
with `pip`:

```bash
pip3 -r requirements.txt
```

Check that Pygame is properly installed with the following Python code:

```python
import pygame

print(pygame.version.ver)
```

You should see output similar to `2.0.0.dev10`.

From now on, when we show code-examples, we'll assume that you have `import pygame` at the top of the file, and we'll
leave it out for brevity's sake.

### 1.2 Launching a window

Pygame is all about graphics, so we want to see something on the screen!

To launch a window, we use a function provided by Pygame's `display` package:

```python
size = (640, 480)
pygame.display.set_mode(size)
```

This program stops running immediately! We have to tell the program to keep running once we have created the window. Try
adding the code below, and run the program. (To stop the program, use Control+C, or the corresponding key combination
for your platform.)

```python
while True:
    pass
```

Now the program keeps running, but we don't see any window! It turns out that we need to interact with the event queue
from Pygame's `event` package for things to get up and running. While you _can_
simply add a call to `pygame.event.get()` before the while-loop (try it if you want), it probably makes more sense to
place the call inside the loop-body (as we'll see later when we want to do more things with events).

If you've followed along so far, you should have code that looks like this:

```python
size = (640, 480)
pygame.display.set_mode(size)

while True:
    pygame.event.get()
```

![Alt text](01-getting-started/screenshots/window.png?raw=true)

Yay, we have a window!

But what if we want to change the background color? In Pygame, graphics are always handled with the `Surface` class (
more on this later). To fill our window with a color, we need a surface that represents the window! We're in luck. It
turns out that the `set_mode` function returns exactly this! Let's get hold the surface and start painting!

```python
size = (640, 480)
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 255))  # fill the screen with color
while True:
    pygame.event.get()
```

You'll notice that this doesn't quite work. The window looks the same as before! I lied slightly before when I said that
this surface represents what is shown on the screen. The surface is more like a "staging area" that you can do whatever
to without it changing what you see on your screen. You have to tell Pygame to actually copy that data to the screen to
see the results! That is done by calling the `update` function from Pygame's `display` package. Let's add
`pygame.display.update()` right after our call to `screen.fill`.

You should now have a window with a blue background!

![Alt text](01-getting-started/screenshots/blue_window.png?raw=true)

How come it's blue? We passed in the tuple
`(0, 0, 255)` to the `fill` method. This is an RGB representation of the color blue. Stated very simply, every pixel on
the screen can be defined by how much of the three colors red (R), green (G), and blue (B)
that it contains. In our case, we set red and green to 0 and blue to 255 which is the max value. Wait, 255 is the max
value? Why couldn't we put 256 or something higher? If we try, we'll be greeted by this error
message: `ValueError: invalid color argument`. The reason we can't go over 255 is that each color is represented by a
_byte_ of data. A byte (which is the same as 8 bits) can express at most 256 (2^8) values and as we're including 0 the
max value will be 255.

So we have a blue window now, but there's a glaring flaw with our window. If you try to close it with the button in the
top corner, nothing happens! We actually need to tell Pygame to stop our program when a user clicks that button. But how
do we know when a user clicks that button (or does anything for that matter)? Remember that "event queue" we mentioned
before? That's how!
The `get` method has been sitting in our while-loop all along, spitting out information about the user's activity. We
just need to use that information!

Let's add some code so that our while-loop looks like this:

```python
while True:
    events = pygame.event.get()
    if events:
        print(events)
```

If you run your updated program, you'll notice that you get bombarded with information as soon as you do anything (press
a button, move the mouse, click with the mouse, etc).

Here is some example outputs that I get when moving my mouse cursor across the screen:

![Alt text](01-getting-started/screenshots/printed_events.png?raw=true)

Let's try to close our window again, and study the output on the command line carefully. You should see output similar
to this:
`[<Event(512-WindowEvent {'event': 14, 'window': None})>, <Event(256-Quit {})>]`

The part that we're particularly interested in is `<Event(256-Quit {})>`. Pygame received an event saying that the user
has requested to close the window! We just need to listen specifically for this event and take action when we see it!
One way to check if an event is a "quit"
event, is to look at its "type" like so: `event.type == pygame.QUIT:`. To shut down our program in a nice way we can
call Pygame's `quit` method and then call `sys.exit(0)` which is a common way of ending Python programs.

Your while-loop should now look like the following:

```python
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
```

(Note that we need to add an import for the `sys` package, just like we've been doing for `pygame`).

Congrats! You now have a window with blue background that can be closed! The complete source code can be
found [here](01-getting-started/02_window.py).

Next, we'll look at doing something more interesting with our window than just showing a blue color indefinitely.

### 1.3 User controlling graphics

To make something that resembles a game even in the slightest, we need to involve the user more!
Let's start with something simple. We'll make the background switch between two different colors whenever the user
presses a key. (While that doesn't sound very exciting in itself, it's a stepping stone.)

Currently, all of our graphics code appears before the while-loop, so it only runs once. To be able to update our
graphics dynamically, let's move our calls to `screen.fill` and
`pygame.display.update` into the while-loop, so that it looks like this:

```python
screen = pygame.display.set_mode(size)
while True:
    screen.fill((0, 0, 255))
    pygame.display.update()
```

Now, we can choose in every iteration of our loop which color to draw. As we want to change the color when a key is
pressed, we need to look for a "key press" event (or `KEYDOWN` as it's called in Pygame). If you add the following to
your event-checking code, you should see that we are able to react to key presses:

```python
if event.type == pygame.KEYDOWN:
    print("A key was pressed!")
```

But we didn't set out to print messages to the console. We want to change the background color!
To prepare for this change, we start by detaching our call to `screen.fill` from the blue color
`(0, 0, 255)`. Update the few lines surrounding `while True` to the following:

```python
colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]
color_index = 0
while True:
    screen.fill(colors[color_index])
```

Run the program to confirm that we didn't break anything. (The program should behave just like before.)

What we've done is to define a list of colors (blue, green, and red) and add an index variable that points to one of the
colors. As it's set to 0 right now, it's pointing at the first color in the list (which happens to be blue). Try
changing the index to `1` and `2` and see how that changes the color on the screen.

So, the only thing we need to do to change the background color in our program is to update this index variable. Let's
replace the print statement we added earlier with this:

```python
color_index = (color_index + 1) % len(colors)
```

That may look complicated, if you aren't familiar with the modulo operator (`%`). What the line is doing is to increment
our index by one but "looping around" to 0 when it reaches `len(colors)`, which is 3 in our case. It's a good thing that
we don't allow the index to reach 3. That would make the program crash when we try to use the index. As lists in Python
are zero-indexed, "index 3"
is just another way of saying "the fourth element in the list", but we only have 3 elements in our list!

If you run the program now, you should see that the background color changes every time you press a key. The complete
source code can be found [here](01-getting-started/03_changing_graphics.py).

Now that we know how to update our graphics based on input from the user, we can do anything!
Well, let's not get ahead of ourselves, but we are truly on a good way toward creating a game.

Next, we'll add an "entity" to our program that can move around on the screen.

### 1.4 Player-controlled entity

In this section, we'll introduce Boxman, a true super hero of game-development. The beauty of Boxman is that he looks
exactly like a rectangle, and therefore is very easy to draw! Let's start by adding some facts about Boxman before our
while-loop:

```python
boxman_color = (100, 150, 200)
boxman = Rect(50, 300, 128, 128)
```

We're giving our hero a nice light blue color, and then we're creating a new `Rect` instance.
`Rect` is a class from Pygame that represents a rectangle. The parameters that we pass in specify the rectangle's
x-position, y-position, width, and height in that order. So we're creating a square that's sitting in the bottom left
corner of our window (assuming the window size is still 640x480).

To draw Boxman, we can add this to our while-loop: `pygame.draw.rect(screen, boxman_color, boxman)`.
`pygame.draw` is a package that provides code for drawing simple geometrical shapes and lines on a surface. We use
the `rect` method (short for rectangle) and pass in the surface that we want to draw on, the color that should be used
for drawing and the rectangle that should be drawn. Make sure to add this method-call immediately after our call
to `screen.fill`. If we were to fill the screen after Boxman has been rendered, his graphics would be drawn over by our
background!

We can also remove all the code involved in updating the background color (assuming that's not a feature we want to keep
around). We might want to hold on the code that listens for key presses though (as we'll connect that to Boxman's
movement later on). If we replace the key press handling with a print statement for now, we should end up with code that
looks something like this:

```python
size = (640, 480)
screen = pygame.display.set_mode(size)
boxman_color = (100, 150, 200)
boxman = Rect(50, 300, 128, 128)
while True:
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, boxman_color, boxman)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            print("Move boxman")
```

If you run the program now, you should see our square-shaped hero idling in the bottom-left corner. How to make him move
though? We can change his position on the screen by updating the x- and y-values on the rectangle, and we are already
listening for key presses. We just need to connect the two. However, we don't want to move Boxman when the user clicks
just any key. Perhaps we should limit ourselves to the WASD keys.

To check which key was pressed, we can use `event.key`. Let's learn what's inside this field by printing it! Change the
print statement to `print(event.key)`. Run the program again, and press down a few keys. You should see numbers
appearing in your command line. Why numbers? That's because the keys are expressed by which "ASCII" value they map to.
For example, if you press the `a` key, you should see the number `97` (as `a` has the code `97` in the ASCII table).
ASCII may be an interesting topic, but for now it's enough to know that Pygame has a numeric code for each of the keys
on your keyboard. So we could write our program in such a way that we compare `event.key`
against these codes, but a better idea is to use constants provided by Pygame so that we don't have to memorize all
these codes. The constant for the `a` key is `pygame.K_a` and the rest of them can usually be guessed easily by their
name.

Now, let's add code for finding WASD key presses and updating the rectangle's position accordingly:

```python
if event.type == pygame.KEYDOWN:
    if event.key == pygame.K_w:
        boxman.y -= 20
    if event.key == pygame.K_a:
        boxman.x -= 20
    if event.key == pygame.K_s:
        boxman.y += 20
    if event.key == pygame.K_d:
        boxman.x += 20
```

If you try out the program now, you should be able to move Boxman around the screen with the WASD keys. However, there
are few quirks that make this game feel quite awkward at the moment. The most noticeable perhaps is that you need to
keep clicking the key to make the movement continue. This may seem surprising, but it has to do with how the event queue
works. The events always correspond to something "changing". For example, if we press the A key, it goes from not being
down to being down. That's a state change that generates a `KEYDOWN` event. If you then release the key, that will
generate a `KEYUP` event. All that time in between, however, no events are generated for this particular key as its
state is not changing. If we want to keep moving Boxman in the subsequent frames after we pressed down the key, we'll
need to remember that the key has been pressed down and perform the movement until we get a `KEYUP` event. Luckily,
there is another way. Pygame already keeps track of all keys that are currently held down. That information is stored in
a huge list that can be accessed with `pygame.key.get_pressed()`. To find out if a particular key is currently held
down, we do a lookup in that list using the key's numeric code. For example, to see if A is held down we
do `pygame.key.get_pressed()[pygame.K_a]`. Let's remove our `KEYDOWN` handling and instead put the following code after
our event for-loop:

```python
if pygame.key.get_pressed()[pygame.K_w]:
    boxman.y -= 20
if pygame.key.get_pressed()[pygame.K_a]:
    boxman.x -= 20
if pygame.key.get_pressed()[pygame.K_s]:
    boxman.y += 20
if pygame.key.get_pressed()[pygame.K_d]:
    boxman.x += 20
```

Try running the program.

Now, that's more like it! Maybe that's a bit too fast though! Let's change `20` to `2`, and while we're at it let's
extract that number to a variable so that we don't have to repeat the same thing 4 times. This will also make it easier
to quickly change the value in the future. Call the variable something informative like `movement_speed` (or `speed` if
you prefer a shorter name).

There is still (at least) one big problem with our movement code. Boxman's movement may be wildly different depending on
how powerful your computer is! We don't have any concept of "time" in our program yet. The program simply runs as fast
as it can. When the frame-rate is higher, we'll be running the code inside of our while-loop more frequently so Boxman
will move faster across the screen. That's generally not what you'd want from a game, so let's try to fix it.

For measuring time, Pygame provides us with a `Clock` class. Let's create a clock instance before entering our while
loop like so: `clock = Clock()`. Inside the while-loop, we'll do
`elapsed_time = clock.tick()` to get the number of milliseconds that have passed since the previous frame. We can now
use this value as a multiplier for our movement and set the distance that Boxman should move according to how much time
has passed: `boxman.x -= elapsed_time * movement_speed`. However, as we're now multiplying our movement speed with a
large number (somewhere around 17 if our game runs at 60 FPS), we'll need to set `movement_speed` to some lower value.
For example, we can set the speed to `0.2` in order to make Boxman move 200 pixels per second
(0.2 pixels * 1000 ms = 200).

Your code should look similar to the following now:

```python
movement_speed = 0.2
clock = Clock()
while True:

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, boxman_color, boxman)
    pygame.display.update()

    # (quit handling omitted for brevity)

    elapsed_time = clock.tick()

    if pygame.key.get_pressed()[pygame.K_w]:
        boxman.y -= elapsed_time * movement_speed
    if pygame.key.get_pressed()[pygame.K_a]:
        boxman.x -= elapsed_time * movement_speed
    if pygame.key.get_pressed()[pygame.K_s]:
        boxman.y += elapsed_time * movement_speed
    if pygame.key.get_pressed()[pygame.K_d]:
        boxman.x += elapsed_time * movement_speed
```

If you run the code now, depending on your frame-rate Boxman's movement may be extremely uneven and jittery. This is
because the `Rectangle` class is storing Boxman's screen position with integer x/y-values. This makes our movement code
very susceptible to rounding issues. Consider for example if during a frame our `elapsed_time` variable is 4. We would
then try to increase the rectangle's x coordinate with 0.8, but `x` being an integer will just round back to its
existing value, meaning that no movement is performed that frame. This can happen several frames in a row if you're
unlucky.

To remedy this issue, let's introduce 2 new variables `x` and `y` that can contain floating numbers. We can then update
these two variables in our movement code and use them for setting the rectangle's position in each frame. The changes
should look something like this.

```python
x, y = 50, 300
boxman = Rect(x, y, 128, 128)

# ...

while True:
    screen.fill((0, 0, 0))
    boxman.topleft = (x, y)
    pygame.draw.rect(screen, boxman_color, boxman)

    # ...

    if pygame.key.get_pressed()[pygame.K_w]:
        y -= elapsed_time * movement_speed

    # ...
```

If you run the program now, you should be able to move Boxman fairly smoothly across the screen. The complete source
code can be found [here](01-getting-started/04_player_controlled_entity.py).

Notice that our while-loop has ended up with three distinct sections, related to handling user input, updating the state
of the game world, and rendering it to the screen. This is a code pattern that is so common in games that it's received
its own name: the "Game Loop"! As you build out your game with more and more shiny features, it may be a good idea to
stick to this 3-step loop (input, update, render), even when the implementation of each said step becomes increasingly
complex. For an *excellent* article on the Game Loop pattern, check
out [this chapter](https://gameprogrammingpatterns.com/game-loop.html) from the _"Game Programming Patterns"_ e-book!

## 2. Advanced topics

TODO