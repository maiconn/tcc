 #!/usr/bin/env python
###########################################################################
# obd_sensors.py
#
# Copyright 2004 Donour Sizemore (donour@uchicago.edu)
# Copyright 2009 Secons Ltd. (www.obdtester.com)
#
# This file is part of pyOBD.
#
# pyOBD is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# pyOBD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyOBD; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###########################################################################
try:
    import wx
    
    EVT_DEBUG_ID = 1010
    
    def debug_display(window, position, message):
        if window is None:
            print message
        else:
            wx.PostEvent(window, DebugEvent([position, message]))
       
    class DebugEvent(wx.PyEvent):
        """Simple event to carry arbitrary result data."""
        def __init__(self, data):
            """Init Result Event."""
            wx.PyEvent.__init__(self)
            self.SetEventType(EVT_DEBUG_ID)
            self.data = data
except ImportError as e:
    def debug_display(window, position, message):
        print message
    
