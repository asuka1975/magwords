import glfw

def get_inch_per_pixel() -> tuple[float, float]:
    inch_per_meter = 39.3701
    monitor = glfw.get_primary_monitor()
    monitor_meter = glfw.get_monitor_physical_size(monitor)
    monitor_inch = (inch_per_meter * monitor_meter[0] * 0.001, inch_per_meter * monitor_meter[1] * 0.001)
    pixel_size = glfw.get_video_mode(monitor).size
    inch_per_pixel = (monitor_inch[0] / pixel_size.width, monitor_inch[1] / pixel_size.height)
    return inch_per_pixel