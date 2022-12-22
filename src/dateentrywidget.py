from tkcalendar import DateEntry

class DateEntryWidget(DateEntry):
    def __init__(self, master=None, align='left', **kw):
        DateEntry.__init__(self, master, **kw)
        self.align = align

    def drop_down(self):
        """Display or withdraw the drop-down calendar depending on its current state."""
        if self._calendar.winfo_ismapped():
            self._top_cal.withdraw()
        else:
            self._validate_date()
            date = self.parse_date(self.get())
            if 'left' in self.align:  # usual DateEntry
                x = self.winfo_rootx()
            if 'center' in self.align:
                x = self.winfo_rootx() + int((self.winfo_width() - self._top_cal.winfo_reqwidth())/2)
            else:  # right aligned drop-down
                x = self.winfo_rootx() + self.winfo_width() - self._top_cal.winfo_reqwidth()
            if 'bottom' in self.align:
                y = self.winfo_rooty() + self.winfo_height()
            else:
                y = self.winfo_rooty() - self._top_cal.winfo_reqheight()

            if self.winfo_toplevel().attributes('-topmost'):
                self._top_cal.attributes('-topmost', True)
            else:
                self._top_cal.attributes('-topmost', False)
            self._top_cal.geometry('+%i+%i' % (x, y))
            self._top_cal.deiconify()
            self._calendar.focus_set()
            self._calendar.selection_set(date)