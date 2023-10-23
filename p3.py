import sys
import random

# Constants for address sizes
VIRTUAL_ADDRESS_SIZE = 4  # Adjust the virtual address size as needed
PHYSICAL_ADDRESS_SIZE = 3 # Adjust the physical address size as needed
PAGE_SIZE = 2
LARGEST_VA_VALUE = 2 ** VIRTUAL_ADDRESS_SIZE - 1
LARGEST_PA_VALUE = 2 ** PHYSICAL_ADDRESS_SIZE - 1
PAGE_TABLE_FILENAME = "ece565f23Q2P3.txt"
DEBUG = True

class Frame:
    def __init__(self, page_num, valid, frame_num):
        self.page_num = page_num
        self.valid = valid
        self.frame_num = frame_num

    

# Global variables
page_table = []
inverse_page_table = [0 for i in range(2 ** PHYSICAL_ADDRESS_SIZE // PAGE_SIZE)]
bitmap = [0 for i in range(2 ** PHYSICAL_ADDRESS_SIZE // PAGE_SIZE)] # sets all frames to 0 because right now they are all free and have not been instantiated
running = True

def generate_virtual_address():
    return random.randint(0, LARGEST_VA_VALUE)

def setup_page_table_and_bitmap():
    with open(PAGE_TABLE_FILENAME, "r") as file:
        for i, line in enumerate(file):
            frame_number, valid_bit = map(int, line.split())
            if valid_bit == 1:
                bitmap[frame_number] = 1 # when it happens upon a frame that is full the zero is switched to 1
                inverse_page_table[frame_number] = Frame(i, valid_bit, frame_number)
    
    for i in range(len(inverse_page_table)):
        if inverse_page_table[i] == 0:
            inverse_page_table[i] = Frame(0, 0, i)

def display_page_table():
    print(bitmap)
    print("Current Invese Page Table")
    for i in range(len(inverse_page_table)):
        print(f"\tFrame: {i}\tPage: {inverse_page_table[i].page_num}\tValid: {inverse_page_table[i].valid}")

def get_free_frame():
    print("page fault occurs", end='')
    for i in range(len(inverse_page_table)):
        print(i)
        if inverse_page_table[i].valid == 0:
            inverse_page_table[i].valid = 1
            bitmap[i] = 1
            return i
        
    print("page replacement needed")
    exit(0)

def access_page_table(page_number):
    
    for i in range(len(inverse_page_table)):
        if inverse_page_table[i].page_num == page_number:
            return inverse_page_table[i].frame_num
    freeFrame = get_free_frame()

    inverse_page_table[freeFrame].frame_num = freeFrame
    inverse_page_table[freeFrame].page_num = page_number
    inverse_page_table[freeFrame].valid = 1

    return freeFrame




# this function checks the bitmap for 0's we just try to access it but we never try to check it before altering it
def check_bitmap():
    if 0 not in bitmap:
            print(" replacement algorithm is needed, call replacement_algo()")
            sys.exit()

# Setup page table and bit map
setup_page_table_and_bitmap()
display_page_table()

try:
    
    while True:
        if DEBUG:
            virtual_address = int(input(f"Enter an {VIRTUAL_ADDRESS_SIZE}-bit virtual address (0-{LARGEST_VA_VALUE}):"))
        else:
            virtual_address = generate_virtual_address()
        print(f"\nVirtual Address = {virtual_address}")

        check_bitmap()

        #if running == False:
            #break
        if 0 <= virtual_address <= LARGEST_VA_VALUE:
            page_number = virtual_address // PAGE_SIZE
            offset = virtual_address % PAGE_SIZE

            frame_number = access_page_table(page_number)

            print(f"\nframe number: {frame_number}")
            print(f"\nthe length is: {len(inverse_page_table)}")
            
            """
            inverse_page_table[frame_number].valid = 1
            inverse_page_table[frame_number].page_num = page_number
            inverse_page_table[frame_number].frame_num = frame_number
            """

            physical_address = inverse_page_table[frame_number].frame_num * PAGE_SIZE + offset 

            print(f"Page number: {page_number}")
            print(f"Frame number: {frame_number}")
            print(f"Physical address: {physical_address}")
            print(bitmap)
            #get_free_frame() this should have been check bitmap, i get it now 

        else:
            print("Invalid input out of range")

except ValueError:
    print("Invalid input. Not a number")