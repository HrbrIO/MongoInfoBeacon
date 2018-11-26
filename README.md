# mongo-beacon
###A simple python beacon for checking Mongo status.

So we wanted to write a really light beacon that would check the status of our Mongo replica sets.  We will keep adding to this but for now it's solely used for sending beacon messages to let us know which server is primary in the replica set.


## Requirements

1. You must have ```python```, ```pip``` and ```pipenv``` installed.
    * You can use other package management systems but you may have to configure yourself.
2. ``mongo`` becaond was designed for `python3` but seems to work just fine with `python2`.


## Usage

1. Clone the repo from Github.
2. Run `pipenv install` to install the dependencies and create a virtual environment.
3. Copy the `example.ini` to `mongo-beacon.ini`.
4. Configure `mongo-beacon.ini` as shown below.
4. Register the `beaconVersionId` in the App in Harbor. The `beaconVersionId` must match the `beaconVersionId` in the in 'mongo-beacon.ini'
5. Fromt the directory you installed the repo run `pipenv run python3 mongo-beacon-py`
6. If you would like to run mongo-beacon as a Linux service we've included a sample systemd service file `example-mongo-beacon.service`.  Here is an easy [guide](https://www.raspberrypi-spy.co.uk/2015/10/how-to-autorun-a-python-script-on-boot-using-systemd/) for running a python script as a service.


## Configuration Options (mongo-beacon.ini)

Two files are used to set options: `options.json` and `options.local.json`. The local file is not included in the repository
as it is usually used to hold sensitive info like API keys. The app will merge the two files on startup, with `options.local.json`
fields taking precendence.

An example JSON options file is shown below.


|     Key     |      Value     |  Required |
|-------------|----------------|-----------|
| apikey | Your Harbor API Key |    yes    |
| appVersionId | The app this Beacon is assigned to. This app must exist in your Harbor account, or beacon messages will be rejected. | yes |
| mongoConnectionString| This is the uri encoded mongo string you use to connect to mongo | yes|
| beaconVersionId | This must match the beaconVersionId registered to the appVersionId in the system | defaults to mongo-beacon:0.1.0 |
| run_interval | How often in seconds the mongo-beacon will check mongo's replica status | defaults to 60 seconds|
| beaconmessagetype| This is a critical field for foghorns and views.  It let's harbor know what type of data is being sent in the beacon message. | defaults to `MONGOINFO`|
| beaconinstanceid | Your chosen beacon instance ID (device or system identifier) or enter `hostname` to use the hostname of your system| no, defaults to `hostname`|
|

## Summary Info

| Item | Value | Comments |
|------|-------|----------|
| Beacon Version ID |  mongo-beacon:0.1.0 |   |
| Beacon Message Type(s) | MONGOINFO | Sends only one type |
| Beacon Instance ID | Defaults to `hostname`|

## Beacon Message Format

Beacon messages sent by this app follow the following data schema:

```
"data": {
    "your-replica-server-1": {
      "isPrimary": 1
    },
    "your-replica-server-2": {
      "isPrimary": 0
    },
    "your-replica-server-3": {
      "isPrimary": 0
    }
