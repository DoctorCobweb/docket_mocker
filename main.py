from escpos.printer import Serial
from escpos.escpos import EscposIO
import random
import datetime as dt
import time


# for usb-to-serial adapter if used
USB_TO_SERIAL_PORT = "/dev/ttyUSB0"

# pcie startech serial card
STANDARD_SERIAL_PORT = "/dev/ttyS4"

# as it appears on physical dockets
areas = [
    "Restaurant Bar",
    "TAB BAR",
    "JUKE BAR",
    "GAMING BAR",
    "SPORTS BAR",
]

# global constants 
PER_ITEM_MAX = 5
ITEM_MAX = 5

def docket_heading (p):
    # TODO: make heading in RED color
    area = areas[random.randint(0, len(areas)-1)]
    p.set(bold=True, double_height=True, double_width=True)
    p.writelines(area)
    p.set(bold=False, double_height=False, double_width=False)

def docket_meta_details(p):
    staff = [
        "BORIS",
        "BORAT",
        "JOHAN",
        "CLAUS",
        "IRIS",
        "ADA",
        "ZARA",
        "SYNTHIA",
    ]

    tablet_num = str(random.randint(1,5))
    staff_member = staff[random.randint(0, len(staff)-1)]
    order_time = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # fixed, dependable content
    p.writelines("Tablet " + tablet_num)
    p.writelines("Clerk: " + staff_member)
    p.writelines(order_time)

    # variable content
    write_table_line(p)
    write_variable_content(p)
    p.writelines("\n")

def write_table_line(p):
    # randomly dropout the table number line; happens when staff order a meal.
    # it's not often so make dropout a rare occurance here.
    # TODO:
    # 1. make table num RED

    table_num = str(random.randint(1,80))
    drop_prob = 0.2

    def write_a_line():
        table_text = ["TABLE No", "ORDER NUMBER"]
        p.set(bold=True)
        table_text_idx = random.randint(0,1)
        if (table_text_idx == 0):
            # "TABLE No *13/0*"
            table_num_text = table_text[table_text_idx] + " *" + table_num + "/0*"
            p.writelines(table_num_text)
        else:
            # "ORDER NUMBER 1"
            table_num_text = table_text[table_text_idx] + " " + table_num
            p.writelines(table_num_text)
        p.set(bold=False)
    if (random.random() < drop_prob):
        # dont print out the table number
        print('DROPPING the table number line. look out')
    else:
        write_table_line()

def write_variable_content(p):
    # most of the time we have a) and b). sometimes c)
    # implement the variable content
    #  a) Name:
    #  b) Covers:
    #  c) extra weird line "PRINT A/C - SARAH @ 11:04"

    drop_prob_1 = 0.2
    drop_prob_1 = 0.1
    covers = str(random.randint(10,20))
    booking_name = [
        "Michelle",
        "Henry",
        "Sarah",
        "Jessica",
        "Douglas",
        "Matthew",
        "Andrew",
        "Stephanie",
        "Kate",
        "Brooke",
        "Phillip",
        "Earnest",
    ]
    booker_name = booking_name[random.randint(0, len(booking_name)-1)]

    if(random.random() < drop_prob_1):
        print('skipping Name: line...')
    else:
        p.writelines("Name: " + booker_name)

    if(random.random() < drop_prob_1):
        print('skipping Covers: line...')
    else:
        p.writelines("Covers: " + covers)

    if(random.random() < drop_prob_2):
        print('skipping ultra random content line...')
    else:
        p.writelines("PRINT A/C - SARAH @ 11:04")

def add_covers(p):
    make_entrees(p)
    make_mains(p)

    # randomly have a dessert
    if (random.random() - 0.2 > 0.5):
        make_dessert(p)

    p.writelines("\n")
    p.writelines("-------------------------------")
    p.writelines("\n")

def make_entrees(p):
    per_item_max = PER_ITEM_MAX
    #num_of_entrees = random.randint(1,3)
    num_of_entrees = ITEM_MAX
    
    entrees = [
        "GARLIC BREAD",
        "OYSTERS NATURAL",
        "OYSTERS KILPATRICK",
        "CRISPY CHIPS",
        "CHILDS FISH AND CHIPS",
        "CHILDS PARMI",
        "CHILDS WHITING",
        "BRUSCHETTA",
        "TASTING PLATE",
        "CHILDS RICE",
        "CHILDS BOLOG",
        "CHILDS BURGER",
        "SWEET POT FRIES",
    ]

    p.set(underline=True)
    p.writelines("ENTREES DINNER")
    p.set(underline=False)
    p.writelines("\n")

    for _ in range(1, num_of_entrees):
        entree_name = entrees[random.randint(1,len(entrees)-1)]
        item_quantity = random.randint(1, per_item_max)
        entree_text = str(item_quantity) + "    " + entree_name
        num_item_extra_info = random.randint(1, item_quantity)

        p.set(bold=True, double_height=True)
        p.writelines(entree_text)
        p.set(bold=False, double_height=False)

        for _ in range(1, num_item_extra_info):
            # make extra content for items
            item_extra_info()

    p.writelines("\n")
    
def make_mains(p):
    per_item_max = PER_ITEM_MAX
    num_of_mains = ITEM_MAX
    # num_of_mains = random.randint(1,3)
    mains = [
        "NASI",
        "EYE",
        "PARMIGIANA",
        "BARRAMUNDI",
        "SALMON",
        "PRAWN RISOTTO",
        "CHILLI CALAMARI",
        "DUCK",
        "MARINATED CHIC",
        "PAPPADELLE LAMB",
        "GNOCCHI",
        "HANGER 200",
        "PORK CUTLET",
        "BIRYANI CURRY",
        "NACHOS",
        "BEEF BURGER",
        "WINTER GREENS",
        "SCOTCH FILLET",
    ]

    p.set(underline=True)
    p.writelines("MAINS DINNER")
    p.set(underline=False)
    p.writelines("\n")

    for _ in range(1, num_of_mains):
        main_name = mains[random.randint(1,len(mains)-1)]
        item_quantity = random.randint(1, per_item_max)
        main_text = str(item_quantity) + "    " + main_name
        num_item_extra_info = random.randint(1, item_quantity)

        p.set(bold=True, double_height=True)
        p.writelines(main_text)
        p.set(bold=False, double_height=False)

        for _ in range(1, num_item_extra_info):
            # make extra content for items
            item_extra_info()

    p.writelines("\n")

def make_dessert(p):
    per_item_max = PER_ITEM_MAX
    #num_of_desserts = random.randomint(1,3)
    num_of_desserts = ITEM_MAX  
    desserts = [
        "STICKY DATE PUDDING",
        "CREME CARAMEL",
        "CHILDS FROG POND",
        "CHILDS MOUSSE",
        "CURROS",
        "FOUNDANT",
    ]

    p.set(underline=True)
    p.writelines("DESSERT")
    p.set(underline=False)
    p.writelines("\n")

    for _ in range(1, num_of_desserts):
        des_name = desserts[random.randint(1,len(desserts)-1)]
        item_quantity = random.randint(1,per_item_max)
        des_text = str(item_quantity) + "    " + des_name
        num_item_extra_info = random.randint(1,item_quantity)

        p.set(bold=True, double_height=True)
        p.writelines(des_text)
        p.set(bold=False, double_height=False)

        for _ in range(1, num_item_extra_info):
            # make extra content for items
            item_extra_info()

    p.writelines("\n")

def item_extra_info():
    p.set(height=1)
    p.writelines("1    MED RARE")
    p.writelines("1    MUSH")
    p.writelines("1    CHIPS GREENS")
    p.writelines("1    XTRA GARLIC BUTT")
    p.writelines("--------------------")



if __name__ == '__main__':
    num_of_dockets = random.randint(1,1)
    print('generating some mock orders')
    print('going to send ' + str(num_of_dockets) + ' dockets')


    for _ in range(0, num_of_dockets):
        # uncomment to add random delay to dockets
        # time.sleep(random.randint(1,5))
        port = Serial(STANDARD_SERIAL_PORT)
        with EscposIO(port) as p:
            docket_heading(p)
            docket_meta_details(p)
            add_covers(p)
        print("should have a docket printed")


    print("finished. all " + str(num_of_dockets) + " dockets sent")
