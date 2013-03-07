# -*- coding: utf-8 -*-
"""
@author: Emilio Moretti
Copyright 2013 Emilio Moretti <emilio.morettiATgmailDOTcom>
This program is distributed under the terms of the GNU Lesser General Public License.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
from InterceptionWrapper import *
import collections,time,threading,Queue

class FunctionRunner(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        while True:
            #grabs a function from queue
            task = self.queue.get()

            #run it
            task.run()
            
            #signals to queue job is done
            self.queue.task_done()
            
class Task(object):
    def __init__(self,autohotpy,f,param):
        self.function = f
        self.arg1 = autohotpy
        self.arg2 = param
    def run(self):
        self.function(self.arg1,self.arg2)
        
class Key(object):
    def __init__(self,auto,code,*args):
        self.auto = auto
        self.code = code
        if (len(args) != 0):
            self.state = args[0]
        else:
            self.state = 0
        self.key_id = auto.get_key_id(self.code, self.state)
        
    def get_id(self):
        return self.key_id
        
    def up(self):
        up = InterceptionKeyStroke()
        up.code = self.code
        up.state = InterceptionKeyState.INTERCEPTION_KEY_UP | self.state
        self.auto.sendToDefaultKeyboard(up)
        
    def press(self):
        event = InterceptionKeyStroke()
        event.code = self.code
        event.state = InterceptionKeyState.INTERCEPTION_KEY_DOWN | self.state
        self.auto.sendToDefaultKeyboard(event)
        self.auto.sleep()
        event.state = InterceptionKeyState.INTERCEPTION_KEY_UP | self.state
        self.auto.sendToDefaultKeyboard(event)
        
    def down(self):
        down = InterceptionKeyStroke()
        down.code = self.code
        down.state = InterceptionKeyState.INTERCEPTION_KEY_DOWN | self.state
        self.auto.sendToDefaultKeyboard(down)
    
    def isPressed(self):
        return not(self.auto.getKeyboardState(self.code,self.state) & InterceptionKeyState.INTERCEPTION_KEY_UP)
    
    def __int__(self):
        return int(self.code)
        
class AutoHotPy(object):
    
    def __init__(self):
        self.exit_configured = False
        
        #default interval between keypress
        self.default_interval = 0.01
        #Threads queue
        self.kb_queue = Queue.Queue()
        self.mouse_queue = Queue.Queue()
        
        # Handlers
        self.keyboard_handler_down = collections.defaultdict(self.__default_element)
        self.keyboard_handler_hold = collections.defaultdict(self.__default_element)
        self.keyboard_handler_up = collections.defaultdict(self.__default_element)
        self.mouse_handler_hold = collections.defaultdict(self.__default_element)
        self.mouse_handler = collections.defaultdict(self.__default_element)
        self.keyboard_state = collections.defaultdict(self.__default_element)
        self.mouse_state = collections.defaultdict(self.__default_element)
        
        
        # Default key scancodes (you can send your own anyway)
        # WARNING! Most of these depend on the keyboard implementation!!!!
        self.ESC=Key(self,0x1)
        self.N1=Key(self,0x2)
        self.N2=Key(self,0x3)
        self.N3=Key(self,0x4)
        self.N4=Key(self,0x5)
        self.N5=Key(self,0x6)
        self.N6=Key(self,0x7)
        self.N7=Key(self,0x8)
        self.N8=Key(self,0x9)
        self.N9=Key(self,0x0A)
        self.N0=Key(self,0x0B)
        self.DASH=Key(self,0x0C)
        #self.Err:520=Key(self,0x0D)
        self.BACKSPACE=Key(self,0x0E)
        self.TAB=Key(self,0x0F)
        self.Q=Key(self,0x10)
        self.W=Key(self,0x11)
        self.E=Key(self,0x12)
        self.R=Key(self,0x13)
        self.T=Key(self,0x14)
        self.Y=Key(self,0x15)
        self.U=Key(self,0x16)
        self.I=Key(self,0x17)
        self.O=Key(self,0x18)
        self.P=Key(self,0x19)
        self.BRACKET_LEFT=Key(self,0x1A)
        self.BRACKET_RIGHT=Key(self,0x1B)
        self.ENTER=Key(self,0x1C)
        self.CTRL=Key(self,0x1D)
        self.A=Key(self,0x1E)
        self.S=Key(self,0x1F)
        self.D=Key(self,0x20)
        self.F=Key(self,0x21)
        self.G=Key(self,0x22)
        self.H=Key(self,0x23)
        self.J=Key(self,0x24)
        self.K=Key(self,0x25)
        self.L=Key(self,0x26)
        self.SEMICOLON=Key(self,0x27)
        self.APOSTROPHE=Key(self,0x28)
        self.GRAVE_ACCENT=Key(self,0x29)
        self.LEFT_SHIFT=Key(self,0x2A)
        self.BACKSLASH=Key(self,0x2B)
        self.Z=Key(self,0x2C)
        self.X=Key(self,0x2D)
        self.C=Key(self,0x2E)
        self.V=Key(self,0x2F)
        self.B=Key(self,0x30)
        self.N=Key(self,0x31)
        self.M=Key(self,0x32)
        self.COMMA=Key(self,0x33)
        self.DOT=Key(self,0x34)
        self.SLASH=Key(self,0x35)
        self.RIGHT_SHIFT=Key(self,0x36)
        self.PRINT_SCREEN=Key(self,0x37)
        self.ALT=Key(self,0x38)
        self.SPACE=Key(self,0x39)
        self.CAPSLOCK=Key(self,0x3A)
        self.F1=Key(self,0x3B)
        self.F2=Key(self,0x3C)
        self.F3=Key(self,0x3D)
        self.F4=Key(self,0x3E)
        self.F5=Key(self,0x3F)
        self.F6=Key(self,0x40)
        self.F7=Key(self,0x41)
        self.F8=Key(self,0x42)
        self.F9=Key(self,0x43)
        self.F10=Key(self,0x44)
        self.NUMLOCK=Key(self,0x45)
        self.SCROLLLOCK=Key(self,0x46)
        self.HOME=Key(self,0x47)
        self.UP_ARROW=Key(self,0x48, InterceptionKeyState.INTERCEPTION_KEY_E0)
        self.PAGE_UP=Key(self,0x49)
        self.DASH_NUM=Key(self,0x4A)
        self.LEFT_ARROW=Key(self,0x4B, InterceptionKeyState.INTERCEPTION_KEY_E0)
        self.NUMERIC_5 =Key(self,0x4C)
        self.RIGHT_ARROW=Key(self,0x4D, InterceptionKeyState.INTERCEPTION_KEY_E0)
        self.PLUS=Key(self,0x4E)
        self.END=Key(self,0x4F)
        self.DOWN_ARROW=Key(self,0x50, InterceptionKeyState.INTERCEPTION_KEY_E0)
        self.PAGE_DOWN=Key(self,0x51)
        self.INSERT=Key(self,0x52)
        self.DELETE=Key(self,0x53)
        self.SHIFT_F1=Key(self,0x54)
        self.SHIFT_F2=Key(self,0x55)
        self.SHIFT_F3=Key(self,0x56)
        self.SHIFT_F4=Key(self,0x57)
        self.SHIFT_F5=Key(self,0x58)
        self.SHIFT_F6=Key(self,0x59)
        self.SHIFT_F7=Key(self,0x5A)
        self.SHIFT_F8=Key(self,0x5B)
        self.SHIFT_F9=Key(self,0x5C)
        self.SHIFT_F10=Key(self,0x5D)
        self.CTRL_F1=Key(self,0x5E)
        self.CTRL_F2=Key(self,0x5F)
        self.CTRL_F3=Key(self,0x60)
        self.CTRL_F4=Key(self,0x61)
        self.CTRL_F5=Key(self,0x62)
        self.CTRL_F6=Key(self,0x63)
        self.CTRL_F7=Key(self,0x64)
        self.CTRL_F8=Key(self,0x65)
        self.CTRL_F9=Key(self,0x66)
        self.CTRL_F10=Key(self,0x67)
        self.ALT_F1=Key(self,0x68)
        self.ALT_F2=Key(self,0x69)
        self.ALT_F3=Key(self,0x6A)
        self.ALT_F4=Key(self,0x6B)
        self.ALT_F5=Key(self,0x6C)
        self.ALT_F6=Key(self,0x6D)
        self.ALT_F7=Key(self,0x6E)
        self.ALT_F8=Key(self,0x6F)
        self.ALT_F9=Key(self,0x70)
        self.ALT_F10=Key(self,0x71)
        self.CTRL_PRINT_SCREEN=Key(self,0x72)
        self.CTRL_LEFT_ARROW=Key(self,0x73)
        self.CTRL_RIGHT_ARROW=Key(self,0x74)
        self.CTRL_END=Key(self,0x75)
        self.CTRL_PAGE_DOWN=Key(self,0x76)
        self.CTRL_HOME=Key(self,0x77)
        self.ALT_1=Key(self,0x78)
        self.ALT_2=Key(self,0x79)
        self.ALT_3=Key(self,0x7A)
        self.ALT_4=Key(self,0x7B)
        self.ALT_5=Key(self,0x7C)
        self.ALT_6=Key(self,0x7D)
        self.ALT_7=Key(self,0x7E)
        self.ALT_8=Key(self,0x7F)
        self.ALT_9=Key(self,0x80)
        self.ALT_0=Key(self,0x81)
        self.ALT_DASH=Key(self,0x82)
        self.ALT_EQUALS=Key(self,0x82)
        self.CTRL_PAGE_UP=Key(self,0x84)
        self.F11=Key(self,0x85)
        self.F12=Key(self,0x86)
        self.SHIFT_F11=Key(self,0x87)
        self.SHIFT_F12=Key(self,0x88)
        self.CTRL_F11=Key(self,0x89)
        self.CTRL_F12=Key(self,0x8A)
        self.ALT_F11=Key(self,0x8B)
        self.ALT_F12=Key(self,0x8C)
        self.CTRL_UP_ARROW=Key(self,0x8C)
        self.CTRL_DASH_NUM=Key(self,0x8E)
        self.CTRL_5_NUM=Key(self,0x8F)
        self.CTRL_PLUS_NUM=Key(self,0x90)
        self.CTRL_DOWN_ARROW=Key(self,0x91)
        self.CTRL_INSERT=Key(self,0x92)
        self.CTRL_DELETE=Key(self,0x93)
        self.CTRL_TAB=Key(self,0x94)
        self.CTRL_SLASH_NUM=Key(self,0x95)
        self.CTRL_ASTERISK_NUM=Key(self,0x96)
        self.ALT_HOME=Key(self,0x97)
        self.ALT_UP_ARROW=Key(self,0x98)
        self.ALT_PAGE_UP=Key(self,0x99)
        #self. =Key(self,0x9A)
        self.ALT_LEFT_ARROW=Key(self,0x9B)
        #self. =Key(self,0x9C)
        self.ALT_RIGHT_ARROW=Key(self,0x9D)
        #self. =Key(self,0x9E)
        self.ALT_END=Key(self,0x9F)
        self.ALT_DOWN_ARROW=Key(self,0xA0)
        self.ALT_PAGE_DOWN=Key(self,0xA1)
        self.ALT_INSERT=Key(self,0xA2)
        self.ALT_DELETE=Key(self,0xA3)
        self.ALT_SLASH_NUM=Key(self,0xA4)
        self.ALT_TAB=Key(self,0xA5)
        self.ALT_ENTER_NUM=Key(self,0xA6)
        
    def get_key_id(self, code, state):
        """
        a key id is a combination of the code and the state ignoring
        up and down bits. This is done to consider E0 and E1 states
        to differentiate left and right control keys, arrows from numbers, etc
        """
        return int("%s%s"% (hex(code).replace('0x', ''),hex(state & 0xFE).replace('0x', '')))
        
    def __default_element(self):
        """
        Used to return None instead of a key exception for maps
        """
        return None
            
    def __null_handler(self,interception,event):
        """
        Used as a null handler to disable events like "hold"
        """
        return None
        
    def sleep(self, *args):
        """
        Sleep. If no parameters are sent, default_interval is assumed.
        useful for waiting between keypress.
        """
        if (len(args) == 0):
            interval = self.default_interval
        else:
            interval=args[0]
        
        time.sleep(interval)
            
    def start(self):
        if (not self.exit_configured):
            raise Exception("Configure a way to close the process before starting")
        #Load the dll and setup the required functions
        self.interception = InterceptionWrapper()
        # Setup context
        self.context = self.interception.interception_create_context()
        if (self.context == None):
            raise Exception("Interception driver not installed!\nInstall required drivers to continue.")
        self.running = True
        
        # Setup filters.
        self.interception.interception_set_filter(self.context, self.interception.interception_is_keyboard, InterceptionFilterKeyState.INTERCEPTION_FILTER_KEY_ALL);
        self.interception.interception_set_filter(self.context, self.interception.interception_is_mouse, InterceptionFilterMouseState.INTERCEPTION_FILTER_MOUSE_ALL);
        
        # Store a default keyboard and a default mouse
        hardware_id = ctypes.c_byte * 512
        for i in range(10):
            current_dev = self.interception.INTERCEPTION_KEYBOARD(i)
            if (self.interception.interception_is_keyboard(current_dev)):
                size = self.interception.interception_get_hardware_id(self.context, current_dev, ctypes.byref(hardware_id()), 512);
                if (size != 0):
                    self.default_keyboard_device = current_dev
                    break
        for i in range(10):
            current_dev = self.interception.INTERCEPTION_MOUSE(i)
            if (self.interception.interception_is_mouse(current_dev)):
                size = self.interception.interception_get_hardware_id(self.context, current_dev, ctypes.byref(hardware_id()), 512);
                if (size != 0):
                    self.default_mouse_device = current_dev
                    break
            
        
        # Start threads. These will run the functions the user writes
        self.kb_thread = FunctionRunner(self.kb_queue)
        self.kb_thread.setDaemon(True)
        self.kb_thread.start()
        self.mouse_thread = FunctionRunner(self.mouse_queue)
        self.mouse_thread.setDaemon(True)
        self.mouse_thread.start()
        stroke = InterceptionStroke()
        
        while (self.running):
            device = self.interception.interception_wait(self.context)
#            print("#####DEVICE ID:"+str(device))
            if (self.interception.interception_receive(self.context, device, ctypes.byref(stroke), 1) > 0):
                if (self.interception.interception_is_keyboard(device)):
                    kb_event=ctypes.cast(stroke, ctypes.POINTER(InterceptionKeyStroke)).contents
                    print("Stroke scancode:" + str(hex(kb_event.code)))
                    print("Stroke state:" + str(hex(kb_event.state)))
                    current_key = self.get_key_id(kb_event.code,kb_event.state)
                    current_state = self.keyboard_state[current_key] #current state for the key
                    self.keyboard_state[current_key] = kb_event.state
                    if (kb_event.state & InterceptionKeyState.INTERCEPTION_KEY_UP): #up
                        user_function = self.keyboard_handler_up[current_key]
                    else:# down
                        if (current_state == kb_event.state):
                            user_function = self.keyboard_handler_hold[current_key]
                        else:
                            user_function = self.keyboard_handler_down[current_key]
                    
                        
                    if (user_function):
                        self.kb_queue.put(Task(self,user_function,kb_event))
                    else:
                        self.interception.interception_send(self.context, device, ctypes.byref(stroke), 1)
                    
                elif (self.interception.interception_is_mouse(device)):
                    mouse_event=ctypes.cast(stroke, ctypes.POINTER(InterceptionMouseStroke)).contents
#                    print("Stroke state:" + str(hex(mouse_event.state)))
#                    print("Stroke flags:" + str(hex(mouse_event.flags)))
#                    print("Stroke information:" + str(hex(mouse_event.information)))
#                    print("Stroke rolling:" + str(hex(mouse_event.rolling)))
#                    print("Stroke x:" + str(hex(mouse_event.x)))
#                    print("Stroke y:" + str(hex(mouse_event.y)))
                    current_state_changed = self.__toggleMouseState(mouse_event)
                    if (current_state_changed):
                        user_function = self.mouse_handler[mouse_event.state]
                    else:
                        user_function = self.mouse_handler_hold[mouse_event.state]
                    
                    if (user_function):
                        self.mouse_queue.put(Task(self,user_function,mouse_event))
                    else:
                        self.interception.interception_send(self.context, device, ctypes.byref(stroke), 1)
                
                
        self.kb_queue.join()
        self.mouse_queue.join()
        self.interception.interception_destroy_context(self.context)
    
    def __toggleMouseState(self, mouse_event):
        """
        applies the mouse state change
        returns False if no changes were made
        """
        BUTTON1=1
        BUTTON2=2
        BUTTON3=3
        BUTTON4=4
        BUTTON5=5
        WHEEL=6
        HWHEEL=7
        newState = mouse_event.state
        if ((newState == InterceptionMouseState.INTERCEPTION_MOUSE_BUTTON_1_DOWN) | (newState == InterceptionMouseState.INTERCEPTION_MOUSE_BUTTON_1_UP)):
            return self.__updateButtonState(BUTTON1,newState)
        elif ((newState == InterceptionMouseState.INTERCEPTION_MOUSE_BUTTON_2_DOWN) | (newState == InterceptionMouseState.INTERCEPTION_MOUSE_BUTTON_2_UP)):
            return self.__updateButtonState(BUTTON2,newState)
        elif ((newState == InterceptionMouseState.INTERCEPTION_MOUSE_BUTTON_3_DOWN) | (newState == InterceptionMouseState.INTERCEPTION_MOUSE_BUTTON_3_UP)):
            return self.__updateButtonState(BUTTON3,newState)
        elif ((newState == InterceptionMouseState.INTERCEPTION_MOUSE_BUTTON_4_DOWN) | (newState == InterceptionMouseState.INTERCEPTION_MOUSE_BUTTON_4_UP)):
            return self.__updateButtonState(BUTTON4,newState)
        elif ((newState == InterceptionMouseState.INTERCEPTION_MOUSE_BUTTON_5_DOWN) | (newState == InterceptionMouseState.INTERCEPTION_MOUSE_BUTTON_5_UP)):
            return self.__updateButtonState(BUTTON5,newState)
        elif (newState == InterceptionMouseState.INTERCEPTION_MOUSE_WHEEL):
            return self.__updateButtonState(WHEEL,mouse_event.rolling)
        elif (newState == InterceptionMouseState.INTERCEPTION_MOUSE_HWHEEL):
            return self.__updateButtonState(HWHEEL,mouse_event.rolling)
            
            
    def __updateButtonState(self, button, newState):
        """
        returns true if the button state has changed
        """
        #Update button 1 if needed
        current_state = self.mouse_state[button]
        if (current_state==newState):
            return False
        else:
            self.mouse_state[button] = newState
            return True
        
    def isRunning(self):
        return self.running
        
    def stop(self):
        self.running = False
        
    def getKeyboardState(self, code, state):
        """
        Return the key state for a given scancode + state mask
        """
        return self.keyboard_state[self.get_key_id(code,state)]
    
    def getMouseState(self, code):
        return self.mouse_state[code]
    
    def registerExit(self, key, handler):
        self.exit_configured = True
        self.keyboard_handler_down[key.get_id()] = handler
        
    def registerForKeyDown(self, key, handler):
        self.keyboard_handler_down[key.get_id()] = handler
    
    def registerForKeyDownAndDisableHoldEvent(self, key, handler):
        self.keyboard_handler_down[key.get_id()] = handler
        self.keyboard_handler_hold[key.get_id()] = self.__null_handler
    
    def registerForKeyUp(self, key, handler):
        self.keyboard_handler_up[key.get_id()] = handler
        
    def registerForKeyHold(self, key, handler):
        self.keyboard_handler_hold[key.get_id()] = handler
    
    def registerForMouseButton(self, key, handler):
        self.mouse_handler[int(key)] = handler
    
    def registerForMouseButtonAndDisableHoldEvent(self, key, handler):
        self.mouse_handler[int(key)] = handler
        self.mouse_handler_hold[int(key)] = self.__null_handler
    
    def registerForMouseButtonHold(self, key, handler):
        self.keyboard_handler_hold[int(key)] = handler
        
    def sendToDefaultMouse(self, stroke):
        self.interception.interception_send(self.context, self.default_mouse_device, ctypes.byref(stroke), 1)
        
    def sendToDefaultKeyboard(self, stroke):
        self.interception.interception_send(self.context, self.default_keyboard_device, ctypes.byref(stroke), 1)    
    
    def sendToDevice(self, device, stroke):
        self.interception.interception_send(self.context, device, ctypes.byref(stroke), 1)    
    
    
