from pynput import mouse


def on_click(x, y, button, pressed):
    if button == mouse.Button.middle and pressed:
        print(f"[{x}, {y}]")


with mouse.Listener(on_click=on_click) as listener:
    listener.join()
