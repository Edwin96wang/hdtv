/*
 * HDTV - A ROOT-based spectrum analysis software
 *  Copyright (C) 2006-2009  The HDTV development team (see file AUTHORS)
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
 
/*
 * This is the ``standard'' peak shape used by the original ``TV'' program.
 * It is described in appendix B of 
 * Jürgen Theuerkauf: Die Analyse von zwei- und mehrdimensionalen
 * γγ-Koinzidenzspektren an Beispielen aus Hochspinexperimenten in der
 * Massengegend um 146Gd (PhD thesis, IKP Cologne, 1994).
 *
 */

#ifndef __Util_h__
#define __Util_h__

#include <string>

namespace HDTV {

std::string GetFuncUniqueName(const char *prefix, void *ptr);

} // end namespace HDTV

#endif
