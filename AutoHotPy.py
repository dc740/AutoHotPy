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
    def __init__(self,f,param):
        self.function = f
        self.arg = param
    def run(self):
        self.function(self.arg)
        
class AutoHotPy(object):
    
    def __init__(self):
        #Load the dll and setup the required functions
        self.interception = InterceptionWrapper()
        # Setup context
        self.context = self.interception.interception_create_context()
        if (self.context == None):
            raise Exception("Interception driver not installed!\nInstall required drivers to continue.")
            
        # Handlers
        
        self.keyboard_handler_down = collections.defaultdict(self.__default_element)
        self.keyboard_handler_hold = collections.defaultdict(self.__default_element)
        self.keyboard_handler_up = collections.defaultdict(self.__default_element)
        self.mouse_handler_hold = collections.defaultdict(self.__default_element)
        self.mouse_handler = collections.defaultdict(self.__default_element)
        self.keyboard_state = collections.defaultdict(self.__default_element)
        self.mouse_state = collections.defaultdict(self.__default_element)
        
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
        
        self.exit_configured = False
        
        #Threads queue
        self.kb_queue = Queue.Queue()
        self.mouse_queue = Queue.Queue()
        
    def __default_element(self):
            return None
            
    def start(self):
        if (not self.exit_configured):
            raise Exception("Configure a way to close the process before starting")
        self.running = True
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
                    current_state = self.keyboard_state[kb_event.code] #current state for the key
                    self.keyboard_state[kb_event.code] = kb_event.state
                    if (kb_event.state & InterceptionKeyState.INTERCEPTION_KEY_UP): #up
                        user_function = self.keyboard_handler_up[kb_event.code]
                    else:# down
                        if (current_state == kb_event.state):
                            user_function = self.keyboard_handler_hold[kb_event.code]
                        else:
                            user_function = self.keyboard_handler_down[kb_event.code]
                    
                        
                    if (user_function):
                        self.kb_queue.put(Task(user_function,kb_event))
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
                        self.mouse_queue.put(Task(user_function,mouse_event))
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
        if (current_state==self.mouse_state[newState]):
            return False
        else:
            self.mouse_state[button] = newState
            return True
        
    def isRunning(self):
        return self.running
        
    def stop(self, event):
        self.running = False
        
    def getKeyboardState(self, code):
        return self.keyboard_state[code]
    
    def getMouseState(self, code):
        return self.mouse_state[code]
    
    def registerExit(self, key):
        self.exit_configured = True
        self.keyboard_handler_down[key] = self.stop
        
    def registerForKeyDown(self, key, handler):
        self.keyboard_handler_down[key] = handler
    
    def registerForKeyUp(self, key, handler):
        self.keyboard_handler_up[key] = handler
        
    def registerForKeyHold(self, key, handler):
        self.keyboard_handler_hold[key] = handler
        
    def sendToDefaultMouse(self, stroke):
        self.interception.interception_send(self.context, self.default_mouse_device, ctypes.byref(stroke), 1)
        
    def sendToDefaultKeyboard(self, stroke):
        self.interception.interception_send(self.context, self.default_keyboard_device, ctypes.byref(stroke), 1)    
    
    def sendToDevice(self, device, stroke):
        self.interception.interception_send(self.context, device, ctypes.byref(stroke), 1)    
    
if __name__=="__main__":
    auto = AutoHotPy()
    SCANCODE_ESC = 0x01
    auto.registerExit(SCANCODE_ESC)
    def abc(event):
        print("Abc running")
        event.code = 0x1e
        auto.sendToDefaultKeyboard(event)
        event.state = 0x01    
        auto.sendToDefaultKeyboard(event)
        time.sleep(1)
        b = InterceptionKeyStroke()
        b.code = 0x30
        b.state = 0x00
        auto.sendToDefaultKeyboard(b)
        b.state = 0x01        
        auto.sendToDefaultKeyboard(b)
        time.sleep(1)
        c = InterceptionKeyStroke()
        c.code = 0x2e
        c.state = 0x00
        auto.sendToDefaultKeyboard(c)
        c.state = 0x01        
        auto.sendToDefaultKeyboard(c)
        

        
    auto.registerForKeyDown(0x2e,abc)
    auto.start()
    
    