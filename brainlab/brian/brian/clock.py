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
"""
Clocks for the simulator
"""

__docformat__ = "restructuredtext en"

__all__ = ['Clock', 'defaultclock', 'guess_clock', 'define_default_clock', 'reinit_default_clock', 'get_default_clock',
           'EventClock', 'RegularClock', 'FloatClock', 'NaiveClock']

from inspect import stack
from units import *
from globalprefs import *
import magic
from time import time
from numpy import ceil


class Clock(magic.InstanceTracker):
    '''
    An object that holds the simulation time and the time step.
    
    Initialisation arguments:
    
    ``dt``
        The time step of the simulation.
    ``t``
        The current time of the clock.
    ``order``
        If two clocks have the same time, the order of the clock is used to
        resolve which clock is processed first, lower orders first.
    ``makedefaultclock``
        Set to ``True`` to make this clock the default clock.
    
    The times returned by this clock are always off the form ``n*dt+offset``
    for integer ``n`` and float ``dt`` and ``offset``. For example, for a clock
    with ``dt=10*ms``, setting ``t=25*ms`` will set ``n=2`` and ``offset=5*ms``.
    For a clock that uses true float values for ``t`` rather than underlying
    integers, use :class:`FloatClock` (although see the caveats there).
    
    In order to make sure that certain operations happen in the correct
    sequence, you can use the ``order`` attribute, clocks with a lower order
    will be processed first if the time is the same. The condition for two
    clocks to be considered as having the same time is
    ``abs(t1-t2)<epsilon*abs(t1)``, a standard test for equality of floating
    point values. For ordinary clocks based on integer times, the value of
    ``epsilon`` is ``1e-14``, and for float based clocks it is ``1e-8``.
    
    The behaviour of clocks was changed in version 1.3 of Brian, if this is
    causing problems you might try using :class:`FloatClock` or if that doesn't
    solve the problem, :class:`NaiveClock`.
    
    **Methods**
    
    .. method:: reinit([t=0*second])
    
        Reinitialises the clock time to zero (or to your
        specified time).
    
    **Attributes**
    
    .. attribute:: t
                   dt
    
        Current time and time step with units.
    
    **Advanced**
    
    *Attributes*
    
    .. attribute:: end
    
        The time at which the current simulation will end,
        set by the :meth:`Network.run` method.
    
    *Methods*
    
    .. method:: tick()
    
        Advances the clock by one time step.
        
    .. method:: set_t(t)
                set_dt(dt)
                set_end(end)
    
        Set the various parameters.
        
    .. method:: get_duration()
    
        The time until the current simulation ends.
        
    .. method:: set_duration(duration)
    
        Set the time until the current simulation ends.
        
    .. method:: still_running()
    
        Returns a ``bool`` to indicate whether the current
        simulation is still running.
    
    For reasons of efficiency, we recommend using the methods
    :meth:`tick`, :meth:`set_duration` and :meth:`still_running`
    (which bypass unit checking internally).
    '''
    @check_units(dt=second, t=second)
    def __init__(self, dt=0.1*msecond, t=0*msecond, order=0,
                 makedefaultclock=False):
        self._gridoffset = 0.0
        self.__dt = 1
        self.dt = dt
        self.t = t
        #self.__t = int(t / dt)
        self.__end = 0
        self.order = order
        if not exists_global_preference('defaultclock') or makedefaultclock:
            set_global_preferences(defaultclock=self)

    @check_units(t=second)
    def reinit(self, t=0 * msecond):
        self.__t = int(float(t) / self._dt)
        self._gridoffset = 0.0

    def __repr__(self):
        return 'Clock: t = ' + str(self.t) + ', dt = ' + str(self.dt)
    __str__ = __repr__

    def tick(self):
        self.__t += self.__dt

    @check_units(t=second)
    def set_t(self, t):
        self.__t = int(float(t) / self._dt)
        self._gridoffset = float(t)-self.__t*self._dt
        #self.__end = int(float(t) / self._dt)

    @check_units(dt=second)
    def set_dt(self, dt):
        self._dt = float(dt)
#        self._dtby2 = self._dt/2.0

    @check_units(end=second)
    def set_end(self, end):
        self.__end = int(float(end) / self._dt)

    @check_units(start=second)
    def set_start(self, start):
        self.__start = int(float(start) / self._dt)

    # Regular clock uses integers, but lots of Brian code extracts _t and _dt
    # directly from the clock, so these should be implemented directly
    _t = property(fget=lambda self:self.__t * self._dt + self._gridoffset)
    _end = property(fget=lambda self:self.__end * self._dt + self._gridoffset)
    _start = property(fget=lambda self:self.__start * self._dt)

    # Clock object internally stores floats, but these properties
    # return quantities
    if isinstance(second, Quantity):
        t = property(fget=lambda self:Quantity.with_dimensions(self._t, second.dim), fset=set_t)
        dt = property(fget=lambda self:Quantity.with_dimensions(self._dt, second.dim), fset=set_dt)
        end = property(fget=lambda self:Quantity.with_dimensions(self._end, second.dim), fset=set_end)
        start = property(fget=lambda self:Quantity.with_dimensions(self._start, second.dim), fset=set_start)
    else:
        t = property(fget=lambda self:self._t, fset=set_t)
        dt = property(fget=lambda self:self._dt, fset=set_dt)
        end = property(fget=lambda self:self._end, fset=set_end)
        start = property(fget=lambda self:self._start, fset=set_start)

    @check_units(duration=second)
    def set_duration(self, duration):
        self.__start = self.__t
        self.__end = self.__t + int(ceil(float(duration) / self._dt))

    def get_duration(self):
        return self.end - self.t

    def still_running(self):
        return self.__t < self.__end

    epsilon = 1e-14

    def __lt__(self, other):
        selft = self._t
        othert = other._t
        if selft==othert: return self.order<other.order
#        if selft<=othert-other._dtby2:
#            return True
        if abs(selft-othert)<=self.epsilon*abs(selft):
            return self.order<other.order
        return selft<othert
    
    
class RegularClock(Clock):
    '''
    Deprecated. Now the same as :class:`Clock`. The old :class:`Clock` class
    is now :class:`FloatClock`.
    '''
    pass


class FloatClock(Clock):
    '''
    Similar to a :class:`Clock` except that it uses a float value of ``t``
    rather than an integer based underlying value. This means that over time
    the values of ``t`` can drift slightly off the grid, and sometimes
    ``t/dt`` will be slightly less than an integer value, sometimes slightly
    more. This can cause problems in cases where the computation ``int(t/dt)``
    is performed to extract an index value, as sometimes an index will be
    repeated or skipped. However, this form of clock can be used for backwards
    compatibility with versions of Brian before the new integer based clock
    was introduced, and for more flexibility than the new version allows for.
    Note also that the equality condition for this clock uses an ``epsilon``
    of ``1e-8`` rather than ``1e-14``. See :class:`Clock` for more details on
    this. For full backwards compatibility with older versions of Brian, use
    :class:`NaiveClock`.
    '''
    _t, _end, _start = 0.0, 0.0, 0.0 # set this here to override the property values defined in Clock
    @check_units(dt=second, t=second)
    def __init__(self, dt=0.1*msecond, t=0*msecond, order=0,
                 makedefaultclock=False):
        self.t = t
        self.dt = dt
        self._end = float(t)
        self.order = order
        if not exists_global_preference('defaultclock') or makedefaultclock:
            set_global_preferences(defaultclock=self)

    @check_units(t=second)
    def reinit(self, t=0 * msecond):
        self._t = float(t)

    def tick(self):
        self._t += self._dt

    @check_units(dt=second)
    def set_dt(self, dt):
        self._dt = float(dt)
#        self._dtby2 = self._dt/2.0

    @check_units(t=second)
    def set_t(self, t):
        self._t = float(t)
        #self._end = float(t)

    @check_units(end=second)
    def set_end(self, end):
        """Sets the end-point for the clock
        """
        self._end = float(end)

    @check_units(start=second)
    def set_start(self, start):
        """Sets the start-point for the clock
        """
        self._start = float(start)

    # Clock object internally stores floats, but these properties
    # return quantities
    if isinstance(second, Quantity):
        t = property(fget=lambda self:Quantity.with_dimensions(self._t, second.dim), fset=set_t)
        dt = property(fget=lambda self:Quantity.with_dimensions(self._dt, second.dim), fset=set_dt)
        end = property(fget=lambda self:Quantity.with_dimensions(self._end, second.dim), fset=set_end)
        start = property(fget=lambda self:Quantity.with_dimensions(self._start, second.dim), fset=set_start)
    else:
        t = property(fget=lambda self:self._t, fset=set_t)
        dt = property(fget=lambda self:self._dt, fset=set_dt)
        end = property(fget=lambda self:self._end, fset=set_end)
        start = property(fget=lambda self:self._start, fset=set_start)

    @check_units(duration=second)
    def set_duration(self, duration):
        """Sets the duration of the clock
        """
        self._start = self._t
        self._end = self._t + float(duration)

    def get_duration(self):
        return self.end - self.t

    def still_running(self):
        """Checks if the clock is still running
        """
        return self._t < self._end

    epsilon = 1e-8


class NaiveClock(FloatClock):
    '''
    Provided for backwards compatibility with older versions of Brian. Does not
    perform any approximate equality tests for clocks, meaning that clock
    processing sequence is undpredictable. Typically, users should use
    :class:`Clock` or :class:`FloatClock`.
    '''
    def __lt__(self, other):
        selft = self._t
        othert = other._t
        if selft==othert:
            return self.order<other.order
        return selft<othert


def guess_clock(clock=None):
    '''
    Tries to guess the clock from global and local namespaces
    from the caller.
    Selects the most local clock.
    Raises an error if several clocks coexist in the same namespace.
    If a non-None clock is passed, then it is returned (simplifies the code).
    '''
    if clock:
        return clock
    # Get variables from the stack
    (clocks, clocknames) = magic.find_instances(Clock)
    if len(clocks) > 1: # several clocks: ambiguous
        # What type of error?
        raise TypeError("Clock is ambiguous. Please specify it explicitly.")
    if len(clocks) == 1:
        return clocks[0]
    # Fall back on default clock
    if exists_global_preference('defaultclock'): return get_global_preference('defaultclock')
    # No clock found
    raise TypeError("No clock found. Please define a clock.")


class EventClock(Clock):
    '''
    Clock that is used for events.
    
    Works the same as a :class:`Clock` except that it is never guessed as a clock to
    use by :class:`NeuronGroup`, etc. These clocks can be used to make multiple clock
    simulations without causing ambiguous clock problems.
    '''
    @staticmethod
    def _track_instances(): return False


# Do not track the default clock    
class DefaultClock(Clock):
    @staticmethod
    def _track_instances(): return False
defaultclock = DefaultClock(dt=0.1 * msecond)
define_global_preference(
    'defaultclock', 'Clock(dt=0.1*msecond)',
    desc="""
         The default clock to use if none is provided or defined
         in any enclosing scope.
         """)


def define_default_clock(**kwds):
    '''
    Create a new default clock
    
    Uses the keywords of the :class:`Clock` initialiser.
    
    Sample usage::
    
        define_default_clock(dt=1*ms)
    '''
    kwds['makedefaultclock'] = True
    newdefaultclock = Clock(**kwds)


def reinit_default_clock(t=0 * msecond):
    '''
    Reinitialise the default clock (to zero or a specified time)
    '''
    get_default_clock().reinit(t)


def get_default_clock():
    '''
    Returns the default clock object.
    '''
    return get_global_preference('defaultclock')

if __name__ == '__main__':
    print id(guess_clock()), id(defaultclock)
