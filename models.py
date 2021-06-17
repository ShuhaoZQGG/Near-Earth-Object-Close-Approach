"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional),diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the
        constructor.
        """

        self.designation = info.get("pdes")
        self.name = info.get("name")
        if self.name == "":
            self.name = None
        self.diameter = info.get("diameter")
        if self.diameter:
            try:
                self.diameter = float(self.diameter)
            except ValueError:
                print("The value has error.")
        else:
            self.diameter = float('nan')

        self.hazardous = info.get("pha")
        if self.hazardous.upper() == 'Y':
            self.hazardous = True
        else:
            self.hazardous = False
        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        if self.name is not None:
            return f"{self.designation} ({self.name})"
        else:
            return self.designation

    def __str__(self):
        """Return `str(self)`."""

        return \
            f"A NearEarthObject {self.fullname}\
                     has a diameter of {float(self.diameter):.3f}\
                         km and the hazardousness is {self.hazardous}"

    def __repr__(self):
        """Return `repr(self)`, a computer-readable \
            string representation of this object."""
        return (f"NearEarthObject(designation={self.designation!r}\
            , name={self.name!r}, "
                f"diameter={float(self.diameter):.3f},\
                     hazardous={self.hazardous!r})")

    def serialize(self):
        return {
            'name': self.name,
            'diameter_km': self.diameter,
            'potentially_hazardous': self.hazardous
        }


class CloseApproach():
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach
    to Earth, such as the date and time (in UTC) of closest approach,
    the nominal approach distance in astronomical units, and the
    relative approach velocity in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied
        to the constructor.
        """

        try:
            self._designation = info.get("des", None)
        except ValueError:
            print("The designation value is falsy")
        try:
            self.time = cd_to_datetime(info.get("cd", None))
        except ValueError:
            print("The time value is falsy")
        try:
            self.distance = info.get("dist", float("nan"))
            self.distance = float(self.distance)
        except ValueError:
            print("The distance value is falsy")
        try:
            self.velocity = info.get("v_rel", float("nan"))
            self.velocity = float(self.velocity)
        except ValueError:
            print("The velocity value is falsy")
        # Create an attribute for the referenced NEO, originally None.
        try:
            self.neo = info.get("neo", None)
        except ValueError:
            print("The neo value is falsy")

    @property
    def fullname(self):
        if self.neo is not None:
            return self.neo
        else:
            return self._designation

    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s
        approach time.

        The value in `self.time` should be a Python `datetime` object.
        While a `datetime` object has a string representation,
        the default representation includes seconds - significant figures
        that don't exist in our input data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """

        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""

        return f"A CloseApproach at {self.time_str},\
             {(self.fullname)} approaches Earth at a distance of\
                  {float(self.distance):.2f} au and a velocity of\
                       {float(self.velocity):.2f} km/s"

    def __repr__(self):
        """Return `repr(self)`, a computer-readable
         string representation of this object."""
        return (f"CloseApproach(time={self.time_str()!r},\
             distance={float(self.distance):.2f}, "
                f"velocity={float(self.velocity):.2f}, neo={self.neo!r})")

    def serialize(self):
        return {
            'designation': self._designation,
            'datetime_utc': self.time_str,
            'distance_au': self.distance,
            'velocity_km_s': self.velocity,
            'neo': self.neo.serialize()
        }
