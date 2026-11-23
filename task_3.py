import asyncio
import numpy as np

from swarms_lab_api.control import gateway

'''
Task 3. (Make the robot move)
(a) Drive forward for two seconds and then backward (reverse mode) for two seconds.
(b) Let the robot move along a square.
(c) Let the robot move along a circle.
'''

async def task_1():
    loop = asyncio.get_running_loop()
    
    print("Connecting to dongle ...")
    dongle = gateway.Gateway(loop, "/dev/ttyACM1", 115200, 0, ["BP-D89C"])

    print("Scanning for robots ...")
    await dongle.scan_and_connect()

    nodes = [*dongle.robots]

    # set yaw to zero
    await nodes[0].reset_yaw()

    # (a)
    print("Driving forwards ...")
    await nodes[0].drive_with_heading(50, 0, 0)
    await asyncio.sleep(2)
    print("Driving backwards ...")
    await nodes[0].drive_with_heading(50, 0, 1)
    await asyncio.sleep(2)

    # (b)
    print("Driving in a square ...")
    for i in range(4):
        await nodes[0].drive_with_heading(50, 90*i, 0)
        await asyncio.sleep(2)

    # (c)
    print("Driving in a circle ...")
    for i in range(359):
        await nodes[0].drive_with_heading(50, i, 0)
        await asyncio.sleep(0.01)


async def main():
    await task_1()

if __name__ == "__main__":
    asyncio.run(main())