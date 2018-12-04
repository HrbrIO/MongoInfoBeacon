# mongo-beacon
### A simple python beacon for checking Mongo status.

So we wanted to write a really light beacon that would check the status of our Mongo replica sets.  We will keep adding to this but for now it's solely used for sending beacon messages to let us know which server is primary in the replica set.


## Requirements

1. You must have ```python```, ```pip``` and ```pipenv``` installed.
 * `python 2.7` and `pip` come standard on MacOS and most Linux distribution.
 * Here is good guide for using 'pipenv' to manage your python project check out this good guide from [Thoughbot](https://robots.thoughtbot.com/how-to-manage-your-python-projects-with-pipenv).
 * You can use other package management systems but you may have to configure yourself.
2. ``mongo`` becaon was designed for `python3` but seems to work just fine with `python2`.


## Installation

1. Clone the repo from Github.
2. Run `pipenv install` from you mongo-beacon directory to install the dependencies and create a virtual environment.
3. Copy the `example.ini` to `mongo-beacon.ini`.
  * The mongo-beacon.ini file has sensitive information so it's ignored as part of the repo.
4. Configure `mongo-beacon.ini` as shown below.
5. Register the `beaconVersionId` in the App in Harbor. The `beaconVersionId` must match the `beaconVersionId` in the in `mongo-beacon.ini`.
6. For directions on how to register a mongo beacon cheack out the [Harbor Quick Start Guide](https://docs.hrbr.io/quick-start-guide/#registering-the-beacon).


## Configuration Options (mongo-beacon.ini)

These are the fields in the `mongo-beacon.ini`:

```css
[apiKey]
apikey = YOUR_API_KEY

[appVersionId]
appversionid = YOUR_APP_VERSION_ID

[mongoConnectionString]
#i.e. mongodb://yourusername:youruserpasswrod@example.com:27017/admin?ssl=true
mongoConnectionString = YOUR_MONGO_CONNECTION_STRING

[default]
#You can change this if you make modifications to the beacon or leave the same if you like my name
beaconversionid = mongo-beacon:0.1.0
#In Seconds
run_interval = 60
#This can be whatever you want but it's easier for Foghrons and Views if it is consistent across systems
beaconmessagetype = MONGOINFO
# If you leave this as hostname it will use the system hostname
beaconinstanceid = hostname
```


|     Key     |      Value     |  Required |
|-------------|----------------|-----------|
| apikey | Your Harbor API Key |    yes    |
| appVersionId | The app this Beacon is assigned to. This app must exist in your Harbor account, or beacon messages will be rejected. | yes |
| mongoConnectionString| This is the uri encoded mongo string you use to connect to mongo | yes|
| beaconVersionId | This must match the beaconVersionId registered to the appVersionId in the system | defaults to mongo-beacon:0.1.0 |
| run_interval | How often in seconds the mongo-beacon will check mongo's replica status | defaults to 60 seconds|
| beaconmessagetype| This is a critical field for foghorns and views.  It let's harbor know what type of data is being sent in the beacon message. | defaults to `MONGOINFO`|
| beaconinstanceid | Your chosen beacon instance ID (device or system identifier) or enter `hostname` to use the hostname of your system| no, defaults to `hostname`|


## Beacon Message Format

Beacon messasges sent by this app follow the following data schema:
```css
"data": {
    "wharf-staging-hrbr-io:27017": {
      "isPrimary": 1
    },
    "wharf-staging-1-hrbr-io:27017": {
      "isPrimary": 0
    },
    "wharf-staging-2-hrbr-io:27017": {
      "isPrimary": 0
    }
  ```
## Run and Schedule the `mongo-info` Beacons

* From the directory you installed the repo run `pipenv run python3 mongo-beacon-py`.
* If you would like to run mongo-beacon as a Linux service we've included a sample systemd service file `example-mongo-beacon.service`.  Here is an easy [guide](https://www.raspberrypi-spy.co.uk/2015/10/how-to-autorun-a-python-script-on-boot-using-systemd/) from for running a python script as a service.

## Test

Go to the the [Cloud Harbor Apps Page](https://cloud.hrbr.io/#!/apps/list) and select the `go to developer console` to check to see if you beacon is actually sending messages.
