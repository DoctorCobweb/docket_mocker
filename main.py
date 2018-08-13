from escpos.printer import Serial
from escpos.escpos import EscposIO
import random
import datetime as dt
import time


# for usb-to-serial adapter if used
USB_TO_SERIAL_PORT = "/dev/ttyUSB0"

# pcie startech serial card
STANDARD_SERIAL_PORT = "/dev/ttyS4"

areas = [
    "Restaurant Bar",
    "Tab Bar",
    "Juke Bar",
    "Gaming Bar",
    "Bottleshop",
]


def docket_heading ():
    area = areas[random.randint(0, len(areas)-1)]
    p.set(bold=True, double_height=True)
    p.writelines(area)
    p.set(bold=False, double_height=False)

def docket_meta_details():
    table_num = random.randint(1,100)
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

    staff_member = staff[random.randint(0, len(staff)-1)]
    order_time = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    tablet_num = str(random.randint(1,5))
    booker_name = booking_name[random.randint(0, len(booking_name)-1)]
    covers = str(314145) + 'FIX'
    table_num = str(random.randint(1,80))

    p.writelines("Tablet " + tablet_num)
    p.writelines("Clerk: " + staff_member)
    p.writelines(order_time)
    p.set(bold=True)
    p.writelines("TABLE No *" + table_num + "/0*")
    p.set(bold=False)
    p.writelines("Name: " + booker_name)
    p.writelines("Covers: " + covers)
    p.writelines("\n")

def add_covers():

    make_entrees()
    make_mains()

    # randomly have a dessert
    if (random.random() - 0.2 > 0.5):
        make_dessert()

    p.writelines("\n")

def make_entrees():
    item_max = 5
    
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

    for _ in range(1,5):
        entree_text = (str(random.randint(1,item_max))
                       + "    "
                       + entrees[random.randint(1,len(entrees)-1)])
        p.writelines(entree_text)
    
def make_mains():
    item_max = 5
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

    for _ in range(1, 10):
        main_text = (str(random.randint(1,item_max))
                     + "    "
                     + mains[random.randint(1,len(mains)-1)])
        p.writelines(main_text)

def make_dessert():
    item_max = 5
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
    p.writelines("\n")

    for _ in range(1, 4):
        des_text = (str(random.randint(1,item_max))
                    + "    "
                    + desserts[random.randint(1,len(desserts)-1)])
        p.writelines(des_text)


if __name__ == '__main__':
    num_of_dockets = random.randint(1,10)
    print('generating some mock orders')
    print('going to send ' + str(num_of_dockets) + ' dockets')

    with EscposIO(Serial(STANDARD_SERIAL_PORT)) as p:

        for _ in range(0, num_of_dockets):
            # uncomment to add random delay to dockets
            # time.sleep(random.randint(1,5))

            docket_heading()
            docket_meta_details()
            add_covers()
            print("should have a docket printed")

    print("finished. all " + str(num_of_dockets) + " dockets sent")
