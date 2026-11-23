import asyncio
import numpy as np

from swarms_lab_api.control import gateway

'''
Task 2. (Light up the matrix)
(a) Display a white frame on the 8×8 matrix.
(b) Define a 4×4 numpy array of 0s and 1s and write a function that iterates through the
array and sets the inner 4×4 grid of the robot’s matrix accordingly (0 = black pixel,
1 = white pixel).
'''

async def task_1():
    loop = asyncio.get_running_loop()
    
    print("Connecting to dongle ...")
    dongle = gateway.Gateway(loop, "/dev/ttyACM1", 115200, 0, ["BP-D89C"])

    print("Scanning for robots ...")
    await dongle.scan_and_connect()

    nodes = [*dongle.robots]

    # (a)
    print("White frame ...")
    for node in nodes:
        await node.set_matrix_line(0, 0, 0, 7, [255, 0, 255])
        await node.set_matrix_line(0, 0, 7, 0, [0, 0, 255])
        await node.set_matrix_line(0, 7, 7, 7, [255, 255, 255])
        await node.set_matrix_line(7, 0, 7, 7, [255, 255, 255])

    await asyncio.sleep(3)

    # (b)
    print("Displaying pattern ...")
    arr = np.array([[0, 1, 0, 1],
                   [1, 0, 1, 0],
                   [0, 1, 0, 1],
                   [1, 0, 1, 0]], np.int8)
    
    offset = 2
    for node in nodes:
        for x in range(4):
            for y in range(4):
                await node.set_matrix_pixel(x +  offset, y + offset, [255, 255, 255] if arr[x][y] else [0, 0, 0])

async def main():
    await task_1()

if __name__ == "__main__":
    asyncio.run(main())