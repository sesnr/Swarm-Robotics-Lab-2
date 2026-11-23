import asyncio
import numpy as np

from swarms_lab_api.control import gateway

'''
Task 1. (Hello world)
(a) Establish a serial connection to the NRF54L15 development kit.
(b) Scan for the advertising name of your robot and connect to it.
(c) Set the robot to sleep mode and wake it up after five seconds.
(d) Blink the robot’s LEDs three times in a color of your choice.
(e) Read the advertising name of the robot and print it to the console.
(f) Read the current battery percentage of the robot and print it to the console.
'''

async def task_1():
    loop = asyncio.get_running_loop()
    
    # (a)
    print("Connecting to dongle ...")
    dongle = gateway.Gateway(loop, "/dev/ttyACM1", 115200, 0, ["BP-D89C"])

    # (b)
    print("Scanning for robots ...")
    await dongle.scan_and_connect()

    nodes = [*dongle.robots]

    # (c)
    print("Knocking robots out ...")
    await asyncio.gather(*[node.sleep() for node in nodes])
    await asyncio.sleep(5)

    print("Waking robots ...")
    await asyncio.gather(*[node.wake() for node in nodes])
    await asyncio.sleep(1)

    # (d)
    print("Blinking robot LEDs ...")
    for i in range(3):
        await asyncio.gather(*[node.set_all_leds([255, 0, 0]) for node in nodes])
        await asyncio.sleep(1)
        await asyncio.gather(*[node.set_all_leds([0, 0, 0]) for node in nodes])
        await asyncio.sleep(1)

    # (e)
    print("Reading robot names ...")
    for node in nodes:
        print((await node.get_bluetooth_advertising_name())["name"])

    # (f)
    print("Reading robot battery percentages ...")
    for node in nodes:
        print((await node.get_battery_percentage())["percentage"])

    # (g) Additionally: name + percentage
    print("Reading robot names and battery percentage ...")
    for node in nodes:
        name = (await node.get_bluetooth_advertising_name())["name"]
        percentage = (await node.get_battery_percentage())["percentage"]
        print(f"{name}: {percentage} %")

async def main():
    await task_1()

if __name__ == "__main__":
    asyncio.run(main())