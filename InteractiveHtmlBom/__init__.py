from generate_interactive_bom import GenerateInteractiveBomPlugin
import pcbnew
import wx
import wx.aui
import threading
import time

plugin = GenerateInteractiveBomPlugin()
plugin.register()


def check_for_bom_button():
    # From Miles McCoo's blog
    # https://kicad.mmccoo.com/2017/03/05/adding-your-own-command-buttons-to-the-pcbnew-gui/
    def find_pcbnew_window():
        windows = wx.GetTopLevelWindows()
        pcbneww = [w for w in windows if "Pcbnew" in w.GetTitle()]
        if len(pcbneww) != 1:
            return None
        return pcbneww[0]

    def callback(_):
        plugin.Run()

    import os
    path = os.path.dirname(__file__)
    bm = wx.Bitmap(path + '/icon.png', wx.BITMAP_TYPE_PNG)
    button_wx_item_id = 0
    while True:
        time.sleep(1)
        pcbwin = find_pcbnew_window()
        if not pcbwin:
            continue

        top_tb = pcbwin.FindWindowById(pcbnew.ID_H_TOOLBAR)
        if button_wx_item_id == 0 or not top_tb.FindTool(button_wx_item_id):
            top_tb.AddSeparator()
            button_wx_item_id = wx.NewId()
            top_tb.AddTool(button_wx_item_id, "iBOM", bm,
                           "Generate interactive BOM", wx.ITEM_NORMAL)
            top_tb.Bind(wx.EVT_TOOL, callback, id=button_wx_item_id)
            top_tb.Realize()


t = threading.Thread(target=check_for_bom_button)
t.daemon = True
t.start()
