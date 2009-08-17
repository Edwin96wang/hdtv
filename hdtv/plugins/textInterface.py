# -*- coding: utf-8 -*-

# HDTV - A ROOT-based spectrum analysis software
#  Copyright (C) 2006-2009  The HDTV development team (see file AUTHORS)
#
# This file is part of HDTV.
#
# HDTV is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# HDTV is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with HDTV; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA

#-------------------------------------------------------------------------------
# TextInterface functions
#-------------------------------------------------------------------------------

import hdtv.options
import os
import pydoc
import sys
import signal

class TextInterface(object):
    
    def __init__(self, height = 25, width = 80):
        
        
        # Set options
        self.opt = dict()
        self.opt["ui.pager.cmd"] = hdtv.options.Option(default = "less") # default pager
        self.opt["ui.pager.args"] = hdtv.options.Option(default = "-F -X") # default pager cmd line options
        
        for (key, opt) in self.opt.items():
            hdtv.options.RegisterOption(key, opt) 

        self._fallback_canvasheight = height
        self._fallback_canvaswidth = width       
        self._updateTerminalSize(None, None)
                    
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self.stdin = sys.stdin
        self.debugout = self.stderr
        
        self.DEBUG_LEVEL = 0
        self.msg("loaded TextInterface")
        signal.signal(signal.SIGWINCH, self._updateTerminalSize)

# TODO: this does not work(?)
#    def __del__(self):
#        signal.signal(signal.SIGWINCH, signal.SIG_IGN) # Restore default signal handler
        
    def page(self, text):
        """
        Print text by pages
        """
        
        cmd = hdtv.options.Get("ui.pager.cmd")
        args = hdtv.options.Get("ui.pager.args")
          
        ret = pydoc.tempfilepager(text, str(cmd) + " " + str(args))

    def msg(self, text, newline = True):
        """
        Message output
        """
        lines = len(text.splitlines())        

        if lines > self.canvasheight:
            self.page(text)
        else:
            self.stdout.write(text)

        if newline:
            self.stdout.write(os.linesep)
            
    def warn(self, text, newline = True):
        """
        Print warning message
        """
        text = "WARNING: " + text
        self.msg(text, newline = newline)
    
    def error(self, text, newline = True):
        """
        Print error message
        """
        text = "ERROR: " + text
        self.msg(text, newline = newline)
    
    
    def debug(self, text, level = 1, newline = True):
      """
      Debugging output. The higher the level, the more specific is the debug message.
      """
      if level > self.DEBUG_LEVEL:
          return
      
      text = "DEBUG: " + text
      self.debugout.write(text)
        
      if newline:
          self.debugout.write(os.linesep)
    
    def newline(self):
        self.msg("", newline = True)
     
    # TODO: Make this work under windows
    def _updateTerminalSize(self, signal, frame):
        def ioctl_GWINSZ(fd):
            try:
                import fcntl, termios, struct, os
                cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
            '1234'))
            except:
                return None
            return cr
        cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
        if not cr:
            try:
                fd = os.open(os.ctermid(), os.O_RDONLY)
                cr = ioctl_GWINSZ(fd)
                os.close(fd)
            except:
                pass
        if not cr:
            try:
                cr = (env['LINES'], env['COLUMNS'])
            except:
                cr = (self._fallback_canvasheight, self._fallback_canvaswidth)

        self.canvasheight = cr[0]
        self.canvaswidth = cr[1]


# initialization
import __main__
if not hasattr(__main__, "ui"):
    __main__.ui = TextInterface()

    
