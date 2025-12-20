from pynput import mouse
import sys

def on_click(x, y, button, pressed):
    """Callback function for mouse clicks."""
    if button == mouse.Button.right and pressed:
        print(f"Right click at coordinates: ({x}, {y})")

def main():
    """Start listening for right mouse clicks."""
    print("Right-click coordinate logger started.")
    print("Right-click anywhere to see the cursor coordinates.")
    print("Press Ctrl+C to stop.\n")
    
    # Create a mouse listener
    with mouse.Listener(on_click=on_click) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            print("\n\nStopped listening for right clicks.")
            sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
#(144, 304)
#akaza(505, 447)
#alucard (498, 473)
#loid (587, 338)