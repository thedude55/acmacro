import win32gui
import win32con
import win32process
import pydirectinput
import pyautogui
import time
import sys

def hover(x, y):
    """Hover over a specified coordinate, then hover over that coordinate + 2 pixels up and to the left."""
    # Hover over the specified coordinate
    pydirectinput.moveTo(x, y)
    time.sleep(0.1)
    
    # Hover over the coordinate + 2 pixels up and to the left (x-2, y-2)
    pydirectinput.moveTo(x - 2, y - 2)
    time.sleep(0.1)

def click(x, y):
    """Left click at specified coordinates using the same hover pattern as roblox_window_manager."""
    hover(x, y)
    pydirectinput.click()

def is_image_on_screen(image_path, confidence=0.9):
    """Check if an image is currently visible on screen.
    
    Args:
        image_path: Path to the image file (e.g., 'startgame.png')
        confidence: Confidence level for image matching (0.0 to 1.0)
    
    Returns:
        bool: True if image is found on screen, False otherwise
    """
    try:
        location = pyautogui.locateOnScreen(image_path, confidence=confidence)
        return location is not None
    except pyautogui.ImageNotFoundException:
        return False
    except Exception:
        return False

def wait_for_image(image_path, timeout=None, confidence=0.9):
    """Wait until the specified image appears on screen.
    
    Args:
        image_path: Path to the image file (e.g., 'startgame.png')
        timeout: Maximum time to wait in seconds (None for infinite)
        confidence: Confidence level for image matching (0.0 to 1.0)
    
    Returns:
        tuple: (x, y) coordinates of the center of the found image, or None if timeout
    """
    print(f"Waiting for image: {image_path}")
    start_time = time.time()
    
    while True:
        try:
            # Try to locate the image on screen
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                # Get the center coordinates of the found image
                center = pyautogui.center(location)
                print(f"Image {image_path} found at: {center} with confidence: {confidence}")
                return center
        except pyautogui.ImageNotFoundException:
            pass
        except Exception as e:
            print(f"Error searching for image: {e}")
        
        # Check for timeout
        if timeout is not None:
            elapsed = time.time() - start_time
            if elapsed >= timeout:
                print(f"Timeout: Image not found after {timeout} seconds")
                return None
        
        time.sleep(0.1)  # Small delay to avoid excessive CPU usage

def find_roblox_window():
    """Find the Roblox window by searching for windows with 'Roblox' in the title."""
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            if 'Roblox' in window_title:
                windows.append((hwnd, window_title))
        return True
    
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows

def focus_window(hwnd):
    """Bring a window to the foreground and focus it."""
    # Restore the window if it's minimized
    if win32gui.IsIconic(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        time.sleep(0.1)
    
    # Bring window to top
    win32gui.SetWindowPos(
        hwnd,
        win32con.HWND_TOP,
        0, 0, 0, 0,
        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
    )
    
    # Try to set foreground window
    try:
        win32gui.SetForegroundWindow(hwnd)
    except Exception:
        # If SetForegroundWindow fails, try alternative method
        try:
            # Get the thread ID of the window
            thread_id = win32process.GetWindowThreadProcessId(hwnd)[0]
            # Attach to the thread's input
            win32process.AttachThreadInput(
                win32process.GetCurrentThreadId(),
                thread_id,
                True
            )
            win32gui.SetForegroundWindow(hwnd)
            win32process.AttachThreadInput(
                win32process.GetCurrentThreadId(),
                thread_id,
                False
            )
        except Exception:
            pass
    
    print("Window focused")

def resize_and_position_window(hwnd, x=10, y=10, width=700, height=400):
    """Resize and position a window."""
    # Get current window style
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
    
    # Remove maximize flag if present
    if style & win32con.WS_MAXIMIZE:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        time.sleep(0.1)
    
    # Move and resize the window
    win32gui.SetWindowPos(
        hwnd,
        win32con.HWND_TOP,
        x, y, width, height,
        win32con.SWP_SHOWWINDOW
    )
    print(f"Window resized to {width}x{height} and positioned at ({x}, {y})")

def setup():
    """Setup the Roblox window: find, resize, position, and focus it."""
    print("Searching for Roblox window...")
    
    # Try to find the window
    roblox_windows = find_roblox_window()
    
    if not roblox_windows:
        print("Roblox window not found. Please make sure Roblox is running.")
        print("Waiting for Roblox window to appear...")
        
        # Wait up to 30 seconds for the window to appear
        for i in range(30):
            time.sleep(1)
            roblox_windows = find_roblox_window()
            if roblox_windows:
                break
            if i % 5 == 0:
                print(f"Still waiting... ({i+1}/30 seconds)")
        
        if not roblox_windows:
            print("Roblox window not found after 30 seconds. Exiting.")
            sys.exit(1)
    
    # If multiple Roblox windows found, use the first one
    hwnd, title = roblox_windows[0]
    print(f"Found Roblox window: '{title}'")
    
    # Resize and position the window
    resize_and_position_window(hwnd, x=10, y=10, width=700, height=400)
    
    # Focus the window
    focus_window(hwnd)
    
    print("Done! Roblox window has been resized, positioned, and focused.")
    return hwnd

def toWinter():
    """Perform the clicks and type 'christ'."""
    # Wait a moment before starting
    time.sleep(1)

    # New coordinates taken from context block (lines 17-23)
    print("Click at coordinates: (63, 324)")
    click(63, 324)
    time.sleep(1)

    print("Click at coordinates: (401, 247)")
    click(401, 247)
    time.sleep(1)

    print("Click at coordinates: (569, 256)")
    click(569, 256)
    time.sleep(1)

    # Type "christ"
    print("Typing 'christ'...")
    pydirectinput.write('christ')
    time.sleep(0.2)

    print("Click at coordinates: (212, 314)")
    click(212, 314)
    time.sleep(1)

    print("Click at coordinates: (336, 356)")
    click(336, 356)
    time.sleep(1)

    print("Click at coordinates: (332, 379)")
    click(332, 379)
    time.sleep(1)

    print("Click at coordinates: (426, 530)")
    click(426, 530)
    time.sleep(1)
    wait_for_image('startgame.png')
    
def orient():
    
    for i in range(10):
        pydirectinput.press('o')
        time.sleep(.1)
    pydirectinput.press('ctrl')
    # Set x, y to the middle coordinates of the Roblox window (700x400 at 10,10 offset)
    x = 10 + 700 // 2
    y = 10 + 400 // 2
    pydirectinput.moveTo(x, y + 400)
    pydirectinput.press('ctrl')
    pydirectinput.keyDown('d')
    time.sleep(2.5)
    pydirectinput.keyUp('d')
    time.sleep(.2)
    pydirectinput.keyDown('w')
    time.sleep(3.5)
    pydirectinput.keyUp('w')
    pydirectinput.press('f')
    print("Done!")
def hover(x, y):
    """Hover over a specified coordinate, then hover over that coordinate + 2 pixels up and to the left."""
    # Hover over the specified coordinate
    pydirectinput.moveTo(x, y)
    time.sleep(0.1)
    
    # Hover over the coordinate + 2 pixels up and to the left (x-2, y-2)
    pydirectinput.moveTo(x - 2, y - 2)
    time.sleep(0.1)
def units():
    click(387, 156)
    time.sleep(5)
    pydirectinput.press('4')
    click(268, 349)
    time.sleep(.2)
    click(648, 182)
    time.sleep(30)
    pydirectinput.press('1')
    click(543, 295)
    time.sleep(15)
    click(775, 186)
    time.sleep(90)
    pydirectinput.press('2')
    click(474, 333)
    click(653, 264)
    time.sleep(100)
    click(603, 258)
    time.sleep(1)
    click(387, 294)
    time.sleep(1)
    click(727, 172)
    time.sleep(125)
    click(386, 294)
    time.sleep(.5)
    hover(438, 336)
    wait_for_image("portal.png")
    pydirectinput.press('f')
    click(405, 620)
def pu():
    click(42, 608)
    time.sleep(.2)
    click(523, 171)
    time.sleep(.2)
    pyautogui.write('lobby')
    time.sleep(.2)
    click(544, 247)
    wait_for_image("units.png")
def pickPortal():
    hover(641, 392)
    if is_image_on_screen("tier11.png"):
        return 3
    hover(380, 434)
    if is_image_on_screen("tier11.png"):
        return 2
    hover(32, 406)
    return 1
def clickPortal(i):
    if i==1:
        click(641, 392)
    elif i==2:
        click(641, 392)
    elif i==3:
        click(641, 392)
    time.sleep(.5)
    click(356, 386)
    time.sleep(.5)
    click(423, 601)
    time.sleep(.5)
    click(237, 479)
    time.sleep(.5)
    click(488, 254)
    time.sleep(.2)
    pydirectinput.write('christ')
    time.sleep(.5)
    click(215, 302)
    time.sleep(.5)
    click(339, 391)
    time.sleep(7)
    pydirectinput.press('f')
if __name__ == "__main__":
    try:
        while True:
            setup()
            toWinter()
            orient()
            if not is_image_on_screen("winter.png"):
                pu()
                continue
            else:
                while True:
                    units()
                    portal = pickPortal()
                    clickPortal(portal)
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

