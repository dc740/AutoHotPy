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
from AutoHotPy import AutoHotPy


def exitAutoHotKey(autohotpy,event):
    """
    exit the program when you press ESC
    """
    autohotpy.stop()
    
def superCombo(autohotpy,event):
    """
    This function is called when you press "A" key.
    It executes the combo: A -> S -> move left -> move up -> A -> S
    """
    autohotpy.A.press()
    autohotpy.S.press()
    autohotpy.LEFT_ARROW.press()
    autohotpy.UP_ARROW.press()
    autohotpy.A.press()
    autohotpy.S.press()

if __name__=="__main__":
    auto = AutoHotPy()
    auto.registerExit(auto.ESC, exitAutoHotKey)   # Registering an end key is mandatory to be able tos top the program gracefully
    # In win7 the task manager is launched when you press Ctrl + Shift + ESC
    # I don't like that. Lets call the task manager when you press Ctrl + Alt + Supr
    auto.registerForKeyDown(auto.A,superCombo)   
    auto.start()
