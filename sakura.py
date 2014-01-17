# -----------------------------------------------------------------------------
#
#   SAKURA,
#      a toolkit to process and average multi-element fluorescence data
#      (currently built for the XAS Beamline at Synchrotron Light Source Australia)
#
# -----------------------------------------------------------------------------
#
#   Authors:
#   Peter Kappen, XAS Beamline
#   Gary Ruben, VeRSI (Victorian eResearch Strategic Initiative)
#
#   Synchrotron Light Source Australia, 2013-2014

# -*- coding: utf-8 -*-

import wx                           # suppress import warning    @UnusedImport
from sakura_ui import SakuraBaseMainFrame
import wx.lib.mixins.inspection


class SakuraWxApp(wx.App, wx.lib.mixins.inspection.InspectionMixin):
    """The main application class - added a wxPython inspection tool
    http://wiki.wxpython.org/Widget%20Inspection%20Tool
    """
    def OnInit(self):
        self.Init()  # initialize the inspection tool
        self.m_frame = SakuraBaseMainFrame(None)
        self.m_frame.Show()
        self.SetTopWindow(self.m_frame)
        return True


if __name__ == '__main__':
    app = SakuraWxApp(0)
    app.MainLoop()
