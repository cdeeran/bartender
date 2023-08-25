'''
Per the pinout schematic.. this is the J8 interface
'''
'''
   3V3  (1) (2)  5V    
 GPIO2  (3) (4)  5V    
 GPIO3  (5) (6)  GND   
 GPIO4  (7) (8)  GPIO14
   GND  (9) (10) GPIO15
GPIO17 (11) (12) GPIO18
GPIO27 (13) (14) GND   
GPIO22 (15) (16) GPIO23
   3V3 (17) (18) GPIO24
GPIO10 (19) (20) GND   
 GPIO9 (21) (22) GPIO25
GPIO11 (23) (24) GPIO8 
   GND (25) (26) GPIO7 
 GPIO0 (27) (28) GPIO1 
 GPIO5 (29) (30) GND   
 GPIO6 (31) (32) GPIO12
GPIO13 (33) (34) GND   
GPIO19 (35) (36) GPIO16
GPIO26 (37) (38) GPIO20
   GND (39) (40) GPIO21
'''


class Pins:

    GPIO_PIN_1 = 1
    GPIO_PIN_2 = 2 # IN USE BY TOUCHSCREEN DO NOT USE
    GPIO_PIN_3 = 3 # IN USE BY TOUCHSCREEN DO NOT USE
    GPIO_PIN_4 = 4
    GPIO_PIN_5 = 5
    GPIO_PIN_6 = 6
    GPIO_PIN_7 = 7
    GPIO_PIN_8 = 8
    GPIO_PIN_9 = 9
    GPIO_PIN_10 = 10
    GPIO_PIN_11 = 11
    GPIO_PIN_12 = 12
    GPIO_PIN_13 = 13
    GPIO_PIN_14 = 14
    GPIO_PIN_15 = 15
    GPIO_PIN_16 = 16
    GPIO_PIN_17 = 17
    GPIO_PIN_18 = 18
    GPIO_PIN_19 = 19
    GPIO_PIN_20 = 20
    GPIO_PIN_21 = 21
    GPIO_PIN_22 = 22
    GPIO_PIN_23 = 23
    GPIO_PIN_24 = 24
    GPIO_PIN_25 = 25
    GPIO_PIN_26 = 26
    GPIO_PIN_27 = 27
    
    GPIO_PINS_LIST = [GPIO_PIN_1,
                      GPIO_PIN_4,
                      GPIO_PIN_5,
                      GPIO_PIN_6,
                      GPIO_PIN_7,
                      GPIO_PIN_8,
                      GPIO_PIN_9,
                      GPIO_PIN_10,
                      GPIO_PIN_11,
                      GPIO_PIN_12,
                      GPIO_PIN_13,
                      GPIO_PIN_14,
                      GPIO_PIN_15,
                      GPIO_PIN_16,
                      GPIO_PIN_17,
                      GPIO_PIN_18,
                      GPIO_PIN_19,
                      GPIO_PIN_20,
                      GPIO_PIN_21,
                      GPIO_PIN_22,
                      GPIO_PIN_23,
                      GPIO_PIN_24,
                      GPIO_PIN_25,
                      GPIO_PIN_26,
                      GPIO_PIN_27]
