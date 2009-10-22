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

# main session of hdtv
import copy

import hdtv.dlmgr
hdtv.dlmgr.LoadLibrary("display")
hdtv.dlmgr.LoadLibrary("fit")

from hdtv.window import Window
from hdtv.drawable import DrawableManager
from hdtv.fitter import Fitter
from hdtv.fit import Fit

class Session(DrawableManager):
    """
    Main session of hdtv
    
    First of all this provides a list of spectra, which is why this is called
    spectra in most contexts. But this also keeps track of the basic fit interface
    and of a list of calibrations.
    """
    def __init__(self):
        self.window = Window() 
        DrawableManager.__init__(self, viewport=self.window.viewport)
        # TODO: make peakModel and bgdeg configurable
        self.defaultFitter = Fitter(peakModel = "theuerkauf", bgdeg = 1)
        self.workFit = Fit(copy.copy(self.defaultFitter))
        import sys
        print sys.getrefcount(self.workFit)
        self.workFit.Draw(self.window.viewport)
        self.caldict = dict()
        # main session is always active
        self._active = True

    def ApplyCalibration(self, specIDs, cal):
        """
        Apply calibration cal to spectra with ids
        """
        # check if ids is list/iterable or just single id 
        try: iter(specIDs)
        except TypeError:
            specIDs = [specIDs]
        for ID in specIDs:
            try:
                spec = self.dict[ID]
            except KeyError:
                hdtv.ui.warn("There is no spectrum with id: %s" % ID)
            else:
                if cal is None:
                    hdtv.ui.msg("Unsetting calibration of spectrum with id %d" % ID)
                else:
                    hdtv.ui.msg("Calibrated spectrum with id %d" % ID)
                spec.cal = cal
                if self.workFit.spec is spec:
                    self.workFit.cal = cal

    # functions to handle the workFot
    def SetFitMarker(self, mtype, pos=None):
        """
        Set Marker of type "mtype" to position pos,
        if pos is not given, the current position of the cursor is used
        """
        if pos is None:
            pos = self.viewport.GetCursorX()
        self.workFit.ChangeMarker(mtype, pos, action="set")
        
    def RemoveFitMarker(self, mtype, pos=None):
        """
        Remove the marker of type "mtype", that is closest to position "pos",
        if position is not given, the current position of the cursor is used
        """ 
        if pos is None:
            pos = self.viewport.GetCursorX()
        self.workFit.ChangeMarker(mtype, pos, action="remove")
        
        
    def ExecuteFit(self, peaks = True):
        """
        Execute the fit
        
        If peaks=False, just an background fit is done, else a peak fit is done. 
        """
        spec = self.GetActiveObject()
        if spec is None:
            hdtv.ui.error("There is no active spectrum")
            return 
        fit = self.workFit
        if not peaks and len(fit.bgMarkers) > 0:
            # pure background fit
            fit.FitBgFunc(spec)
        if peaks:
            # full fit
            fit.FitPeakFunc(spec)
        fit.Draw(self.window.viewport)

    def ClearFit(self, bg_only=False):
        """
        Clear the markers and erase a previously executed fit.
        
        If bg_only is True, only the background fit is cleared and a peak fit
        is repeated now with internal background.
        """
        if bg_only:
            self.workFit.bgMarkers.Clear()
            self.workFit.Erase(bg_only)
            self.workFit.Refresh()
        else:
            self.workFit.bgMarkers.Clear()
            self.workFit.peakMarkers.Clear()
            self.workFit.regionMarkers.Clear()
            self.workFit.spec = None
        
    def ActivateFit(self, ID, sid=None):
        """
        Copy markers of a already stored fit to workFit.
        
        Note: that a call to Store will overwrite the active fit withworkFit
        """
        if sid is None:
            sid = self.activeID
        if sid is None:
            hdtv.ui.warn("There is no active spectrum")
            return
        spec = self.dict[sid]
        spec.ActivateObject(ID)
        if ID is not None:
            # make a copy for workFit
            self.workFit = copy.copy(spec.GetActiveObject())
            self.workFit.active = True
            self.workFit.Draw(self.window.viewport)

    def StoreFit(self, ID=None):
        """
        Stores current workFit with ID.
        
        If no ID is given, the next free ID is used.
        The markers are kept in workFit, so that one can re-use.
        """ 
        spec = self.workFit.spec
        if spec is None:
            hdtv.ui.warn("No fit available to store")
            return
        ID = spec.Insert(self.workFit, ID=spec.activeID)
        spec.dict[ID].active = False
        spec.ActivateObject(None)
        hdtv.ui.msg("Storing workFit with ID %s" % ID)
        self.workFit = copy.copy(self.workFit)
        self.workFit.Draw(self.window.viewport)
        

    # Overwrite some functions of DrawableManager to do some extra work
    def ActivateObject(self, ID):
        """
        Activate Object and reset workFit when activating another spectrum
        """
        if ID is not self.activeID:
            # reset workFit
            self.workFit.spec = None
            # deactivate a possible active fit
            spec = self.GetActiveObject()
            if spec is not None:
                spec.ActivateObject(None)
        DrawableManager.ActivateObject(self, ID)
        

    def Pop(self, ID):
        """
        Pop spectrum with ID and activate prevID if ID was activeID
        """
        if self.activeID is ID:
            self.ActivateObject(self.prevID)
        return DrawableManager.Pop(self, ID)

            
    def ShowObjects(self, ids, clear=True):
        """
        Show spectra and make sure one of the visible objects is active
        """
        DrawableManager.ShowObjects(self, ids, clear)
        if self.activeID not in self.visible:
            if len(self.visible)>0:
                self.ActivateObject(max(self.visible))
            else:
                self.ActivateObject(None)
                
    def HideObjects(self, ids):
        """
        Hide spectra and make sure one of the visible objects is active
        """
        DrawableManager.HideObjects(self, ids)
        if self.activeID not in self.visible:
            if len(self.visible)>0:
                self.ActivateObject(max(self.visible))
            else:
                self.ActivateObject(None)
        
        

