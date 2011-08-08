# ----------------------------------------------------------------------------------
# Copyright ENS, INRIA, CNRS
# Contributors: Romain Brette (brette@di.ens.fr) and Dan Goodman (goodman@di.ens.fr)
# 
# Brian is a computer program whose purpose is to simulate models
# of biological neural networks.
# 
# This software is governed by the CeCILL license under French law and
# abiding by the rules of distribution of free software.  You can  use, 
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info". 
# 
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability. 
# 
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or 
# data to be ensured and,  more generally, to use and operate it in the 
# same conditions as regards security. 
# 
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
# ----------------------------------------------------------------------------------
# 
######### PHYSICAL UNIT NAMES #####################
#------------------------------------ Dan Goodman -
# These are optional shorthand unit names which in
# most circumstances shouldn't clash with local names

"""Optional short unit names

This module defines the following short unit names:

mV, mA, uA (micro_amp), nA, pA, mF, uF, nF, mS, uS, ms,
Hz, kHz, MHz, cm, cm2, cm3, mm, mm2, mm3, um, um2, um3
"""

import units as _units

mV = _units.mvolt

mA = _units.mamp
uA = _units.uamp
nA = _units.namp
pA = _units.pamp

pF = _units.pfarad
uF = _units.ufarad
nF = _units.nfarad

nS = _units.nsiemens
uS = _units.usiemens

ms = _units.msecond

Hz = _units.hertz
kHz = _units.khertz
MHz = _units.Mhertz

cm = _units.cmetre
cm2 = _units.cmetre2
cm3 = _units.cmetre3
mm = _units.mmetre
mm2 = _units.mmetre2
mm3 = _units.mmetre3
um = _units.umetre
um2 = _units.umetre2
um3 = _units.umetre3

_units.all_units.extend([mV, mA, uA, nA, pA, pF, uF, nF, nS, uS, ms, Hz, kHz, MHz, cm, cm2, cm3, mm, mm2, mm3, um, um2, um3])
