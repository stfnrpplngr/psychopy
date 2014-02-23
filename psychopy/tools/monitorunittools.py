#!/usr/bin/env python2

# Part of the PsychoPy library
# Copyright (C) 2014 Jonathan Peirce
# Distributed under the terms of the GNU General Public License (GPL).

'''Functions and classes related to unit conversion respective to a particular
monitor'''

from psychopy import monitors

# Maps supported coordinate unit type names to the function that converts
# the given unit type to PsychoPy OpenGL pix unit space.
_unit2PixMappings = dict()

#the following are to be used by convertToPix
def pix2pix(vertices, pos, win = None):
    return pos+vertices
_unit2PixMappings['pix'] = pix2pix

def _cm2pix(vertices, pos, win):
    return cm2pix(pos+vertices, win.monitor)
_unit2PixMappings['cm'] = _cm2pix

def _deg2pix(vertices, pos, win):
    return deg2pix(pos+vertices, win.monitor)
_unit2PixMappings['deg'] = _deg2pix

def _degFlatPos2pix(vertices, pos, win):
    posCorrected = deg2pix(pos, win.monitor, correctFlat=True)
    vertices = deg2pix(vertices, win.monitor, correctFlat=False)
    return posCorrected+vertices
_unit2PixMappings['degFlatPos'] = _degFlatPos2pix

def _degFlat2pix(vertices, pos, win):
    return deg2pix(pos+vertices, win.monitor, correctFlat=True)
_unit2PixMappings['degFlat'] = _degFlat2pix

def _norm2pix(vertices, pos, win):
    return (pos+vertices) * win.size/2.0
_unit2PixMappings['norm'] = norm2pix

def _height2pix(vertices, pos, win):
    return (pos+vertices) * win.size[1]
_unit2PixMappings['height'] = height2pix

def convertToPix(vertices, pos, units, win):
    """Takes vertices and position, combines and converts to pixels from any unit

    The reason that `pos` and `vertices` are provided separately is that it allows
    the conversion from deg to apply flat-screen correction to each separately.

    The reason that these use function args rather than relying on self.pos
    is that some stimuli (e.g. ElementArrayStim use other terms like fieldPos)
    """
    unit2pix_func = _unit2PixMappings.get(units)
    if unit2pix_func:
        return unit2pix_func(vertices, pos, win)
    else:
        raise ValueError("The unit type [{0}] is not registered with PsychoPy".format(units))

def addUnitTypeConversion(unit_label, mapping_func):
    """
    Add support for converting units specified by unit_label to pixels to be
    used by convertToPix (therefore a valid unit for your PsychoPy stimuli)

    mapping_func must have the function prototype:

    def mapping_func(vertices, pos, win):
        # Convert the input vertices, pos to pixel positions PsychoPy will use
        # for OpenGL call.

        # unit type -> pixel mapping logic here
        # .....

        return pix
    """
    if unit_label in unit2PixMappings:
        raise ValueError("The unit type label [{0}] is already registered with PsychoPy".format(unit_label))
    unit2PixMappings[unit_label]=mapping_func

#
# Built in conversion functions follow ...
#

def cm2deg(cm, monitor):
    """Convert size in cm to size in degrees for a given Monitor object"""
    #check we have a monitor
    if not isinstance(monitor, monitors.Monitor):
        raise ValueError("cm2deg requires a monitors.Monitor object as the second argument but received %s" %str(type(monitor)))
    #get monitor dimensions
    dist = monitor.getDistance()
    #check they all exist
    if dist==None:
        raise ValueError("Monitor %s has no known distance (SEE MONITOR CENTER)" %monitor.name)
    return cm/(dist*0.017455)


def deg2cm(degrees, monitor):
    """Convert size in degrees to size in pixels for a given Monitor object"""
    #check we have a monitor
    if not isinstance(monitor, monitors.Monitor):
        raise ValueError("deg2cm requires a monitors.Monitor object as the second argument but received %s" %str(type(monitor)))
    #get monitor dimensions
    dist = monitor.getDistance()
    #check they all exist
    if dist==None:
        raise ValueError("Monitor %s has no known distance (SEE MONITOR CENTER)" %monitor.name)
    return degrees*dist*0.017455


def cm2pix(cm, monitor):
    """Convert size in degrees to size in pixels for a given Monitor object"""
    #check we have a monitor
    if not isinstance(monitor, monitors.Monitor):
        raise ValueError("cm2pix requires a monitors.Monitor object as the second argument but received %s" %str(type(monitor)))
    #get monitor params and raise error if necess
    scrWidthCm = monitor.getWidth()
    scrSizePix = monitor.getSizePix()
    if scrSizePix==None:
        raise ValueError("Monitor %s has no known size in pixels (SEE MONITOR CENTER)" %monitor.name)
    if scrWidthCm==None:
        raise ValueError("Monitor %s has no known width in cm (SEE MONITOR CENTER)" %monitor.name)

    return cm*scrSizePix[0]/float(scrWidthCm)


def pix2cm(pixels, monitor):
    """Convert size in pixels to size in cm for a given Monitor object"""
    #check we have a monitor
    if not isinstance(monitor, monitors.Monitor):
        raise ValueError("cm2pix requires a monitors.Monitor object as the second argument but received %s" %str(type(monitor)))
    #get monitor params and raise error if necess
    scrWidthCm = monitor.getWidth()
    scrSizePix = monitor.getSizePix()
    if scrSizePix==None:
        raise ValueError("Monitor %s has no known size in pixels (SEE MONITOR CENTER)" %monitor.name)
    if scrWidthCm==None:
        raise ValueError("Monitor %s has no known width in cm (SEE MONITOR CENTER)" %monitor.name)
    return pixels*float(scrWidthCm)/scrSizePix[0]


def deg2pix(degrees, monitor):
    """Convert size in degrees to size in pixels for a given Monitor object"""
    #get monitor params and raise error if necess
    scrWidthCm = monitor.getWidth()
    scrSizePix = monitor.getSizePix()
    if scrSizePix==None:
        raise ValueError("Monitor %s has no known size in pixels (SEE MONITOR CENTER)" %monitor.name)
    if scrWidthCm==None:
        raise ValueError("Monitor %s has no known width in cm (SEE MONITOR CENTER)" %monitor.name)

    cmSize = deg2cm(degrees, monitor)
    return cmSize*scrSizePix[0]/float(scrWidthCm)


def pix2deg(pixels, monitor):
    """Convert size in pixels to size in degrees for a given Monitor object"""
    #get monitor params and raise error if necess
    scrWidthCm = monitor.getWidth()
    scrSizePix = monitor.getSizePix()
    if scrSizePix==None:
        raise ValueError("Monitor %s has no known size in pixels (SEE MONITOR CENTER)" %monitor.name)
    if scrWidthCm==None:
        raise ValueError("Monitor %s has no known width in cm (SEE MONITOR CENTER)" %monitor.name)
    cmSize=pixels*float(scrWidthCm)/scrSizePix[0]
    return cm2deg(cmSize, monitor)
