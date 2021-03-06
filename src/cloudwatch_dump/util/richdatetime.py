import calendar
from datetime import datetime, timedelta
from dateutil.tz import tzlocal
import pytz


class RichDateTime(datetime):
    """Enriched datetime class."""

    def __new__(cls, year, month=None, day=None, hour=0, minute=0, second=0, microsecond=0, tzinfo=None):
        if tzinfo is None:
            raise ValueError('tzinfo must be specified')
        return datetime.__new__(cls, year, month, day, hour, minute, second, microsecond, tzinfo)

    def epoch(self):
        """Convert native or aware datetime to epoch time."""
        return calendar.timegm(self.timetuple())

    def to_local(self):
        """Return new instance with local timezone."""
        return self.from_datetime(self, tzlocal())

    def to_utc(self):
        """Return new instance with utc timezone."""
        return self.from_datetime(self, pytz.utc)

    def __mod__(self, time_unit):
        """Cut remainder of modulus by time_unit"""
        if not isinstance(time_unit, timedelta):
            raise TypeError('time_unit must be instance of datetime.timedelta')
        total_seconds = time_unit.seconds + time_unit.days * 24 * 3600
        if total_seconds <= 0:
            raise ValueError('time_unit must be greater or equal than one second')
        rem = self.epoch() % total_seconds
        return self.from_datetime(self - timedelta(seconds=rem, microseconds=self.microsecond))

    @classmethod
    def from_datetime(cls, dt, tzinfo=None):
        """Return RichDateTime instance from datetime instance."""
        if tzinfo:
            if dt.tzinfo:  # dt is aware
                dt = dt.astimezone(tzinfo)
            else:  # dt is naive
                try:  # localize() is much nicer than replace
                    dt = tzinfo.localize(dt)
                except:
                    dt = dt.replace(tzinfo=tzinfo)
        return RichDateTime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond, dt.tzinfo)

    @classmethod
    def now(cls, tzinfo=tzlocal()):
        """Get current datetime with timezone info."""
        return cls.from_datetime(datetime.now(tzinfo))

    @classmethod
    def strptime(cls, date_string, format, tzinfo=tzlocal()):
        """Return an aware datetime corresponding to date_string, parsed according to format."""
        return cls.from_datetime(datetime.strptime(date_string, format), tzinfo=tzinfo)
