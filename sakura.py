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
#   Synchrotron Light Source Australia, 2013

# -*- coding: utf-8 -*-

import wx
from sakura_ui import SakuraBaseMainFrame


class SakuraWxApp(wx.App):
    def OnInit(self):
        self.m_frame = SakuraBaseMainFrame(None)
        self.m_frame.Show()
        self.SetTopWindow(self.m_frame)
        return True


if __name__ == '__main__':
    app = SakuraWxApp(0)
    app.MainLoop()
