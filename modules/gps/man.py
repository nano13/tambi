
module_description = """
This module provides some gps related functionality like showing the current position or logging.

On Linux gpsd is prefered as the backend, which of course has to be set up and running, and of course you need a gps-device.
"""

position = """
Returns the GPS-position of the device this software is running on.

On Linux gpsd ist used as the backend, which of course has to be set up and running (and of course you need a gps-device for this).

Other Operating Systems (like Windows or Mac) are not supported yet.
"""

start_log = """
Starts the gps-logging. The log is saved to a sqlite3-database named UNIXTIMESTAMP.sqlite
"""

stop_log = """
Stops the gps-logging.
"""

logs = """
Shows a simple list of the logs.
"""

plot = """
Plots the specified gps log source.

@param (required): [string], the filename of the gps log.

See Also:
gps.logs
gps.start_log
gps.stop_log
"""
