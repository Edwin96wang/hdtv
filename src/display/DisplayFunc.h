/*
 * HDTV - A ROOT-based spectrum analysis software
 *  Copyright (C) 2006-2009  Norbert Braun <n.braun@ikp.uni-koeln.de>
 *
 * This file is part of HDTV.
 *
 * HDTV is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the
 * Free Software Foundation; either version 2 of the License, or (at your
 * option) any later version.
 *
 * HDTV is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
 * for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with HDTV; if not, write to the Free Software Foundation,
 * Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
 * 
 */

#ifndef __DisplayFunc_h__
#define __DisplayFunc_h__

#include <TF1.h>
#include "Painter.h"
#include "DisplayObj.h"

namespace HDTV {
namespace Display {

class DisplayFunc : public DisplayObj {
  public:
  	DisplayFunc(const TF1 *func, int col = DEFAULT_COLOR);
  	  	
  	inline TF1 *GetFunc()  { return fFunc; }
  	inline double Eval(double x)  { return fFunc->Eval(x); }
  	
  	inline double GetMinCh(void) { double min, max; fFunc->GetRange(min, max); return min; }
    inline double GetMaxCh(void) { double min, max; fFunc->GetRange(min, max); return max; }
    
    // HDTV::Display:: required for CINT
    virtual std::list<HDTV::Display::DisplayObj *>& GetList(DisplayStack *stack);
    
    virtual void PaintRegion(UInt_t x1, UInt_t x2, Painter& painter)
      { if(IsVisible()) painter.DrawFunction(this, x1, x2); }
  	
  private:
  	TF1 *fFunc;
};

} // end namespace Display
} // end namespace HDTV

#endif
