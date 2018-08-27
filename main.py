from escpos.printer import Serial
from escpos.escpos import EscposIO
import random
import datetime as dt
import time
import menuItems as mi



#------------------------------------------------------------
# GLOBALS AND SERIAL PORT REFERENCE
#------------------------------------------------------------

# for usb-to-serial adapter if used
USB_TO_SERIAL_PORT = "/dev/ttyUSB0"

# pcie startech serial card
STANDARD_SERIAL_PORT = "/dev/ttyS4"

# as it appears on physical dockets
areas = mi.docketStartFields

# global constants 
PER_ITEM_MAX = 4
ITEM_MAX = 3
p = Serial(STANDARD_SERIAL_PORT)



#------------------------------------------------------------
# DOCKET HEADER AND META DETAILS
#------------------------------------------------------------

def docket_heading ():
    area = areas[random.randint(0, len(areas)-1)]
    p.set(bold=True, double_height=True, double_width=True)
    red_color()
    p.text("{0}\n".format(area))
    black_color()
    p.set(bold=False, double_height=False, double_width=False)

def docket_meta_details():
    staff = mi.staff

    tablet_num = str(random.randint(1,5))
    staff_member = staff[random.randint(0, len(staff)-1)]
    order_time = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # fixed, dependable content
    p.text("Tablet {0}\n".format(tablet_num))
    p.text("Clerk: {}\n".format(staff_member))
    p.text("{0}\n".format(order_time))

    # variable content
    write_table_line()
    write_variable_content()

def write_table_line():
    # randomly dropout the table number line; happens when staff order a meal.
    # it's not often so make dropout a rare occurance here.

    table_num = str(random.randint(1,80))
    drop_prob = 0.2

    def write_a_line():
        table_text = ["TABLE No", "ORDER NUMBER"]
        p.set(bold=True)
        table_text_idx = random.randint(0,1)
        if (table_text_idx == 0):
            # "TABLE No *13/0*"
            table_num_text = "{0} *{1}/0*\n".format(table_text[table_text_idx],table_num)
            red_color()
            p.text(table_num_text)
            black_color()
        else:
            # "ORDER NUMBER 1"
            table_num_text = "{0} {1}\n".format(table_text[table_text_idx], table_num)
            red_color()
            p.text(table_num_text)
            black_color()
        p.set(bold=False)
    if (random.random() < drop_prob):
        # dont print out the table number
        print('DROPPING the table number line. look out')
    else:
        write_a_line()

def write_variable_content():
    # most of the time we have a) and b). sometimes c)
    # implement the variable content
    #  a) Name:
    #  b) Covers:
    #  c) extra weird line "PRINT A/C - SARAH @ 11:04"

    drop_prob_1 = 0.2
    drop_prob_2 = 0.1
    covers = str(random.randint(10,20))
    booking_name = mi.bookingName
    booker_name = booking_name[random.randint(0, len(booking_name)-1)]

    if(random.random() < drop_prob_1):
        print('DROPPING Name: line...')
    else:
        p.text("Name: {0}\n".format(booker_name))

    if(random.random() < drop_prob_1):
        print('DROPPING Covers: line...')
    else:
        p.text("Covers: {0}\n".format(covers))

    if(random.random() < drop_prob_2):
        print('DROPPING ultra random content line...')
    else:
        p.text("\n")
        p.text("PRINT A/C - SARAH @ 11:04\n")
        p.text("\n")



#------------------------------------------------------------
# DOCKET COURSES AND ITEM INFOS 
#------------------------------------------------------------

def make_entrees():
    entrees = mi.entrees
    write_course_field("ENTREES DINNER")
    write_menu_items(entrees, entrees_item_extra_info)
    p.text("\n")
    
def make_mains():
    mains = mi.mains
    write_course_field("MAINS DINNER")
    write_menu_items(mains, mains_item_extra_info)
    p.text("\n")

def make_desserts():
    desserts = mi.desserts
    write_course_field("DESSERT")
    write_menu_items(desserts, dessert_item_extra_info)
    p.text("\n")

def make_call_away_docket():
    cad = mi.callAwayDocket

    write_course_field(cad["course_field"])

    p.set(bold=True, double_height=True)
    p.text("{0}\n".format(cad["menu_item"]))
    p.set(bold=False, double_height=False)

    p.set(height=1)
    p.text("{0}\n".format(cad["info"][0]))
    p.text("  --------------------\n")

def make_standard_docket():
    # standard docket is entrees, mains, and sometimes desserts.
    make_entrees()
    make_mains()

    # randomly have a dessert
    if (random.random() < 0.8):
        make_desserts()
    else:
        print('DROPPING dessert')

def make_edge_case_docket():
    write_course_field("BAR MEALS")
    p.set(bold=True, double_height=True)
    p.text("add gravy")
    p.text("\n")
    p.text("for the band")
    p.set(bold=False, double_height=False)

    make_mains()

def make_empty_docket():
    write_course_field("SPECIAL INSTRUCTIONS")


def make_dessert_docket():
    per_item_max = PER_ITEM_MAX
    num_of_desserts = ITEM_MAX  
    desserts = mi.desserts

    write_course_field("DESSERT")
    write_menu_items(desserts, dessert_item_extra_info)

    write_course_field("CHILDS MENU")

    p.set(bold=True, double_height=True)
    p.text("4    CHILDS ICE CREAM\n")
    p.set(bold=False, double_height=False)

    p.set(bold=True, double_height=True)
    p.text("2    CHILDS FROG POND\n")
    p.set(bold=False, double_height=False)

    write_course_field("CHILD DESSERT TOPS")

    p.set(bold=True, double_height=True)
    p.text("2    CHOCO TOPPING\n")
    p.set(bold=False, double_height=False)

def write_course_field(text):
    p.set(underline=True)
    p.text("{0}\n".format(text))
    p.set(underline=False)
    p.text("\n")

def write_menu_items(items, item_info_fn):
    num_of_items = ITEM_MAX
    per_item_max = PER_ITEM_MAX

    if (not item_info_fn):
        raise Exception('ERROR: no item_info_fn supplied')

    for _ in range(1, num_of_items):
        item_name = items[random.randint(1,len(items)-1)]
        item_quantity = random.randint(1,per_item_max)
        item_text = "{0}    {1}\n".format(str(item_quantity), item_name)
        num_item_extra_info = random.randint(1,item_quantity)

        p.set(bold=True, double_height=True)
        p.text(item_text)
        p.set(bold=False, double_height=False)

        for _ in range(1, num_item_extra_info):
            # make extra content for items
            item_info_fn()

def entrees_item_extra_info():
    p.set(height=1)
    if (random.random() < 0.5):
        p.text("1    ex cheese\n")
        p.text("1    no pepper\n")
        p.text("1    add jalepenos\n")
        p.text("  --------------------\n")
    else:
        p.text("1    no salt\n")
        p.text("1    gluten free\n")
        p.text("  --------------------\n")

def mains_item_extra_info():
    p.set(height=1)
    if (random.random() <0.5):
        p.text("1    MED RARE\n")
        p.text("1    MUSH\n")
        p.text("1    CHIPS GREENS\n")
        p.text("1    XTRA GARLIC BUTT\n")
        p.text("  --------------------\n")
    else:
        p.text("1    WELL DONE\n")
        p.text("1    pep sce o/s\n")
        p.text("  --------------------\n")


def dessert_item_extra_info():
    p.set(height=1)
    if (random.random() < 0.5):
        p.text("1    LEMON SCE\n")
        p.text("1    ex scoop\n")
        p.text("  --------------------\n")
    else:
        p.text("1    with sorbet instead\n")
        p.text("1    ex cold\n")
        p.text("1    sprinkles o/s\n")
        p.text("  --------------------\n")



#------------------------------------------------------------
# DOCKET UTILITY FUNCTIONS
#------------------------------------------------------------

def red_color():
    p._raw(b'\x1b' + b'\x72\x01')

def black_color():
    p._raw(b'\x1b' + b'\x72\x00')


if __name__ == '__main__':
    num_of_dockets = random.randint(1,1)
    print('generating some mock orders')
    print('going to send ' + str(num_of_dockets) + ' dockets')


    for _ in range(0, num_of_dockets):
        # uncomment to add random delay to dockets
        # time.sleep(random.randint(1,5))
        docket_heading()
        docket_meta_details()

        if (random.random() <0.01):
            print("EDGE CASE docket")
            make_edge_case_docket()
        elif (random.random() < 0.8):
            print("MAKE EMPTY docket")
            make_empty_docket()
        elif (random.random() < 0.2):
            # send a call away docket
            print("CALL AWAY docket")
            make_call_away_docket()
        elif (random.random() < 0.8):
            # make a standard docket
            print("STANDARD docket")
            make_standard_docket()
        else:
            # make a solely dessert docket
            print("DESSERT docket")
            make_dessert_docket()

        p.text("\n\n")
        p.text("-------------------------------\n")
        p.cut()
        print("should have a docket printed")

    print("finished. all " + str(num_of_dockets) + " dockets sent")
