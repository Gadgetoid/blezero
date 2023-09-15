import uasyncio as asyncio
from blezero import Device, Sensor, IRRADIANCE, TEMPERATURE, PRESSURE, HUMIDITY
from picographics import PicoGraphics, PEN_RGB555 as PEN

"""
In this example weather data from the Enviro weather(https://shop.pimoroni.com/products/enviro-weather-board-only) and indoor(https://shop.pimoroni.com/products/enviro-indoor) devices is displayed on a HDMI screen
A bar graph of each sensor on a given device is drawn and its respective data is frequently updated 

"""
graphics = PicoGraphics(width=640, height=480, pen_type=PEN)
WIDTH, HEIGHT = graphics.get_bounds()

WHITE = graphics.create_pen(255, 255, 255)
BLACK = graphics.create_pen(0, 0, 0)
RED = graphics.create_pen(255, 0, 0)
GREEN = graphics.create_pen(0, 255, 0)
BLUE = graphics.create_pen(0, 0, 255)
YELLOW = graphics.create_pen(255, 255, 0)
TEAL = graphics.create_pen(0, 255, 255)
PURPLE = graphics.create_pen(255, 0, 255)


graphics.set_pen(TEAL)
graphics.clear()
graphics.set_pen(RED)
graphics.text("BUFFER 1", 0, 0, 4)
graphics.update()

graphics.set_pen(TEAL)
graphics.clear()
graphics.set_pen(RED)
graphics.text("BUFFER 2", 0, 0, 4)
graphics.update()

print("Cleared...")

devices = (
    Device(
        'enviro-indoor',
        Sensor("Light", 160, IRRADIANCE, drange=None),
        Sensor("Temp", 160, TEMPERATURE, drange=(20, 40)),
        Sensor("Pressure", 160, PRESSURE, drange=(1000, 1100)),
        Sensor("Humidity", 160, HUMIDITY, drange=(0, 100))
    ),
    Device(
        'enviro-weather',
        Sensor("Light", 160, IRRADIANCE, drange=None),
        Sensor("Temp", 160, TEMPERATURE, drange=(20, 40)),
        Sensor("Pressure", 160, PRESSURE, drange=(1000, 1100)),
        Sensor("Humidity", 160, HUMIDITY, drange=(0, 100))
    )
)

async def main():
    while True:
       
        for device in devices:
            await device.update()

        await refresh_display()
        await asyncio.sleep_ms(1000)


async def refresh_display():
    print("Display draw...")

    graphics.set_pen(BLACK)
    graphics.clear()
    W = int(WIDTH // 2)
    H = int(HEIGHT // 4)

    GW = W - 4 - 20
    GH = H - 4 - 20
    graphics.set_pen(WHITE)
    text1_width = graphics.measure_text(f"{devices[0].name}", scale=2)
    graphics.text(f"{devices[0].name}", WIDTH//2 - text1_width//2, 0, scale = 2)
    devices[0].sensors[0].draw_graph(graphics, 0+22, 0+16, GW, GH, BLUE, WHITE)
    devices[0].sensors[1].draw_graph(graphics, W+12, 0+16, GW, GH, RED, WHITE)
    devices[0].sensors[2].draw_graph(graphics, 0+22, H+2, GW, GH, GREEN, WHITE)
    devices[0].sensors[3].draw_graph(graphics, W+12, H+2, GW, GH, TEAL, WHITE)
    
    graphics.line(0, HEIGHT//2, WIDTH, HEIGHT//2)
    
    text2_width = graphics.measure_text(f"{devices[1].name}", scale=2)
    graphics.text(f"{devices[1].name}", WIDTH//2 - text2_width//2, HEIGHT//2 + 2, scale = 2)
    devices[1].sensors[0].draw_graph(graphics, 0+22, (H*2)+0+16, GW, GH, BLUE, WHITE)
    devices[1].sensors[1].draw_graph(graphics, W+12, (H*2)+0+16, GW, GH, RED, WHITE)
    devices[1].sensors[2].draw_graph(graphics, 0+22, (H*2)+H+2, GW, GH, GREEN, WHITE)
    devices[1].sensors[3].draw_graph(graphics, W+12, (H*2)+H+2, GW, GH, TEAL, WHITE)
    
    print("Display update...")
    graphics.update()



asyncio.run(main())