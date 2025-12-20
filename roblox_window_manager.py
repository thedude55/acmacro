import win32gui
import win32con
import win32process
import pydirectinput
import pyautogui
import time
import sys

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

def hover(x, y):
    """Hover over a specified coordinate, then hover over that coordinate + 2 pixels up and to the left."""
    # Hover over the specified coordinate
    pydirectinput.moveTo(x, y)
    time.sleep(0.1)
    
    # Hover over the coordinate + 2 pixels up and to the left (x-2, y-2)
    pydirectinput.moveTo(x - 2, y - 2)
    time.sleep(0.1)
def click(x, y):
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
def lobbyToHalloween():
    click(789, 482) #area
    time.sleep(1)
    click(337, 324) #challenges
    time.sleep(2)
    click(752, 130)#click to zoom
    for i in range(10):#zoom out
        pydirectinput.press('o')
        time.sleep(.1)
    click(227, 167)#halloween
    time.sleep(.5)
    pydirectinput.press('e')#enter halloween
    time.sleep(3)
    click(424, 534)#dracula text
    time.sleep(.2)
    click(483, 481)#play
    time.sleep(.1)
    click(352, 357)
    time.sleep(.1)
    click(409, 529)
def pu():
    click(42, 608)
    time.sleep(.2)
    click(523, 171)
    time.sleep(.2)
    pyautogui.write('lobby')
    time.sleep(.2)
    click(544, 247)
    wait_for_image("units.png")
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
    pump = is_image_on_screen("pumpkin.png")
    print(pump)
    if pump:
        pu()
        return False
    return True
def units1():
    pydirectinput.press('5')
    click(513, 269)
    time.sleep(.2)
    pydirectinput.press('2')
    click(502, 445)
    time.sleep(3)
    pydirectinput.press('1')
    click(477, 522)
    time.sleep(.2)
    wait_for_image("pickcard.png")
    time.sleep(2)
    choose()
    time.sleep(3)
    pydirectinput.press('4')
    click(373, 536)
    time.sleep(.2)
    pydirectinput.press('4')
    click(389, 462)
    time.sleep(.2)
    pydirectinput.press('4')
    click(449, 194)
    time.sleep(.2)
    pydirectinput.press('6')
    click(506, 325)
    time.sleep(.2)
    pydirectinput.press('6')
    click(527, 307)
    time.sleep(.2)
    pydirectinput.press('6')
    click(541, 335)
    time.sleep(.2)
    pydirectinput.press('6')
    click(478, 244)
    time.sleep(.2)
    click(650, 186)
    time.sleep(.2)
    click(725,262)
    time.sleep(.2)
    click(400,300)

    for i in range(2):
        wait_for_image("pickcard.png")
        time.sleep(2)
        choose()
    click(772, 184)
    time.sleep(.2)
    click(651, 270)
    for i in range(5):
        wait_for_image("pickcard.png")
        time.sleep(2)
        choose()
    # Block for click function insertion with 0.2s cooldown (sleep)
    click(731, 174)
    time.sleep(.2)
    click(390, 293)
    time.sleep(.2)
    click(771, 267)
    time.sleep(.2)
    click(647, 351)
    time.sleep(.2)
    click(771, 353)
    time.sleep(.2)
    click(656, 441)
    time.sleep(.2)
    click(770, 435)
    time.sleep(.2)
    click(647, 524)
    time.sleep(.2)
    click(775, 522)
    time.sleep(.2)
    click(600, 270)
    time.sleep(.2)
    click(391, 298)
    print("looping now")
    while True:
        if is_image_on_screen("replay.png"):
            print(f"replay.png detected with confidence: 0.9")
            break
        
        # Then check for pickcard.png
        if is_image_on_screen("pickcard.png"):
            print(f"pickcard.png detected with confidence: 0.9")
            time.sleep(2)
            choose()
        time.sleep(0.2)
def choose():
    """Look for images in order, click the first one found, then click pickcard.png"""
    order = ['health3.png','health2.png','health1.png',"tradeoff1.png"]
    
    found_image = False
    # Search for images in order
    for image_path in order:
        try:
            # Try to locate the image on screen
            location = pyautogui.locateOnScreen(image_path, confidence=0.9)
            if location:
                # Get the center coordinates of the found image
                center = pyautogui.center(location)
                x, y = int(center.x), int(center.y)
                print(f"Found {image_path} at: ({x}, {y}) with confidence: 0.9")
                # Click on the found image
                click(x, y)
                time.sleep(0.3)
                found_image = True
                break
            
        except pyautogui.ImageNotFoundException:
            print(f"{image_path} not found, trying next...")
            continue
        except Exception as e:
            print(f"Error searching for {image_path}: {e}")
            continue
    
        
    if not found_image:
        click(610, 328)
        time.sleep(0.3)
        print("No images from the order list were found on screen")
    
    # Click on pickcard.png location
    time.sleep(0.5)  # Give time for pickcard to appear
    try:
        pickcard_location = pyautogui.locateOnScreen("select.png", confidence=0.9)
        if pickcard_location:
            pickcard_center = pyautogui.center(pickcard_location)
            x, y = int(pickcard_center.x), int(pickcard_center.y)
            print(f"Found select.png at: ({x}, {y}) with confidence: 0.9")
            click(x, y)
        else:
            print("pickcard.png not found on screen")
    except pyautogui.ImageNotFoundException:
        print("pickcard.png not found on screen")
    except Exception as e:
        print(f"Error searching for pickcard.png: {e}")
def restart():
    time.sleep(1)
    click(289, 484)
    time.sleep(5)
def main():
    setup()
    while True:

        lobbyToHalloween()
        wait_for_image("startgame.png")
        time.sleep(5)
        if not orient():
            print("restarting setup")
            time.sleep(5)
            continue
        
        pydirectinput.press('f')
        time.sleep(3)
        c = 0
        while True:
            c+=1
            if c == 20:
                pu()
                break
            click(382, 159)
            time.sleep(5)
            units1()
            restart()
            time.sleep(5)
            
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
#(144, 304)
#akaza ()
