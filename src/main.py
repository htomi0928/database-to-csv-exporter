import configparser
import mysql.connector
import wx
import wx.grid as grd
import csv


# Define a custom grid class
class MyGrid(grd.Grid):
    def __init__(self, parent):
        grd.Grid.__init__(self, parent, -1, size=(400, 150))
        self.size = len(tables)
        self.cb = None
        self.CreateGrid(self.size, 2)
        self.RowLabelSize = 20
        self.ColLabelSize = 20

        # Making checkbox column
        attr = grd.GridCellAttr()
        attr.SetEditor(grd.GridCellBoolEditor())
        attr.SetRenderer(grd.GridCellBoolRenderer())
        self.SetColAttr(0, attr)
        self.SetColSize(0, 20)
        self.SetColSize(1, 300)

        # Bind events
        self.Bind(grd.EVT_GRID_CELL_LEFT_CLICK, self.onMouse)
        self.Bind(grd.EVT_GRID_SELECT_CELL, self.onCellSelected)
        self.Bind(grd.EVT_GRID_EDITOR_CREATED, self.onEditorCreated)

        # Add table names to column
        x = 0
        for item in tables:
            self.SetCellValue(x, 1, item[0])
            x += 1

    # Functions for the checkboxes to work
    def onMouse(self, evt):
        if evt.Col == 0:
            wx.CallLater(100, self.toggleCheckBox)
        evt.Skip()

    def toggleCheckBox(self):
        self.cb.Value = not self.cb.Value

    def onCellSelected(self, evt):
        if evt.Col == 0:
            wx.CallAfter(self.EnableCellEditControl)
        evt.Skip()

    def onEditorCreated(self, evt):
        if evt.Col == 0:
            self.cb = evt.Control
            self.cb.WindowStyle |= wx.WANTS_CHARS
            self.cb.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        evt.Skip()

    def onKeyDown(self, evt):
        if evt.KeyCode == wx.WXK_UP:
            if self.GridCursorRow > 0:
                self.DisableCellEditControl()
                self.MoveCursorUp(False)
        elif evt.KeyCode == wx.WXK_DOWN:
            if self.GridCursorRow < (self.NumberRows - 1):
                self.DisableCellEditControl()
                self.MoveCursorDown(False)
        elif evt.KeyCode == wx.WXK_LEFT:
            if self.GridCursorCol > 0:
                self.DisableCellEditControl()
                self.MoveCursorLeft(False)
        elif evt.KeyCode == wx.WXK_RIGHT:
            if self.GridCursorCol < (self.NumberCols - 1):
                self.DisableCellEditControl()
                self.MoveCursorRight(False)
        else:
            evt.Skip()

    # Get list of selected table names
    def getTables(self):
        selectedTables = []
        for index in range(self.size):
            if self.GetCellValue(index, 0) == "1":
                selectedTables.append(self.GetCellValue(index, 1))
        return selectedTables


# Custom frame class
class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Database converter")
        panel = wx.Panel(self, style=0)
        self.grid = MyGrid(panel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 1, wx.EXPAND)
        panel.SetSizer(sizer)

        sizer2 = wx.BoxSizer(wx.VERTICAL)
        button = wx.Button(panel, label='Save')
        button.Bind(wx.EVT_BUTTON, self.Save)
        sizer2.Add(button)
        sizer.Add(sizer2, 2, wx.EXPAND)

        self.grid.SetFocus()

    # Save selected tables to csv file
    def Save(self, _):
        selectedTables = self.grid.getTables()
        print(selectedTables)
        for table in selectedTables:
            cursor.execute(f"select * from {table}")
            rows = cursor.fetchall()
            fp = open(f'out/{table}.csv', 'w')
            myFile = csv.writer(fp)
            myFile.writerows(rows)
            fp.close()


# Define the application class
class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None)
        frame.Show(True)
        self.SetTopWindow(frame)
        return True


# Main program
if __name__ == '__main__':
    # Read config file
    config = configparser.ConfigParser()
    config.read('config/db_config.ini')

    host = config["Config"]["Host"]
    user = config["Config"]["User"]
    password = config["Config"]["Password"]
    database = config["Config"]["Database"]

    # Connect to database
    db = (mysql.connector.connect(host=host, user=user, passwd=password, database=database))

    # Fetch database tables
    cursor = db.cursor()
    cursor.execute("show tables")
    tables = cursor.fetchall()

    # Run the wxPython app
    MyApp(0).MainLoop()
