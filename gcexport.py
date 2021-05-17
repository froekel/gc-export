#!/usr/bin/env python3

from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
    GarminConnectAuthenticationError,
)

from datetime import date
import os,zipfile,sys
from os import listdir
"""
Enable debug logging
"""
import logging
logging.basicConfig(level=logging.DEBUG)

today = date.today()


"""
Based on args, load for user
"""
print("Running for user : %s" % sys.argv[1] )
print("----------------------------------------------------------------------------------------")

userName = sys.argv[1]
password = sys.argv[2]
nrActivities = sys.argv[3]
"""
Initialize Garmin client with credentials
Only needed when your program is initialized
"""
print("Garmin(email, password)")
print("----------------------------------------------------------------------------------------")
try:
    client = Garmin(userName, password)
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client init: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client init")
    quit()


"""
Login to Garmin Connect portal
Only needed at start of your program
The library will try to relogin when session expires
"""
print("client.login()")
print("----------------------------------------------------------------------------------------")
try:
    client.login()
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client login: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client login")
    quit()


"""
Get full name from profile
"""
print("client.get_full_name()")
print("----------------------------------------------------------------------------------------")
try:
    print(client.get_full_name())
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get full name: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get full name")
    quit()


"""
Get activities data
"""
print("client.get_activities(0,1)")
print("----------------------------------------------------------------------------------------")
try:
    activities = client.get_activities(0,nrActivities) # 0=start, 1=limit
    print(activities)
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get activities: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get activities")
    quit()


"""
Download an Activity
"""
try:
    for activity in activities:
        activity_id = activity["activityId"]
        print("client.download_activities(%s)", activity_id)
        print("----------------------------------------------------------------------------------------")

        # gpx_data = client.download_activity(activity_id, dl_fmt=client.ActivityDownloadFormat.GPX)
        # output_file = f"./{str(activity_id)}.gpx"
        # with open(output_file, "wb") as fb:
        #     fb.write(gpx_data)

        # tcx_data = client.download_activity(activity_id, dl_fmt=client.ActivityDownloadFormat.TCX)
        # output_file = f"./{str(activity_id)}.tcx"
        # with open(output_file, "wb") as fb:
        #     fb.write(tcx_data)

        zip_data = client.download_activity(activity_id, dl_fmt=client.ActivityDownloadFormat.ORIGINAL)
        output_file = f"./zips/{str(activity_id)}.zip"
        with open(output_file, "wb") as fb:
            fb.write(zip_data)

        # csv_data = client.download_activity(activity_id, dl_fmt=client.ActivityDownloadFormat.CSV)
        # output_file = f"./{str(activity_id)}.csv"
        # with open(output_file, "wb") as fb:
        #   fb.write(csv_data)
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get activity data: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get activity data")
    quit()


first_activity_id = activities[0].get("activityId")
owner_display_name =  activities[0].get("ownerDisplayName")


# now unzip files
appRoot = os.getcwd()
zipDir = '\\zips'
extension = ".zip"
zips = appRoot + zipDir
os.chdir(zips) # change directory from working dir to dir with files

for item in os.listdir(zips): # loop through items in dir
    if item.endswith(extension): # check for ".zip" extension
        file_name = os.path.abspath(item) # get full path of files
        zip_ref = zipfile.ZipFile(file_name) # create zipfile object
        zip_ref.extractall(appRoot) # extract file to dir
        zip_ref.close() # close file
        os.remove(file_name) # delete zipped file