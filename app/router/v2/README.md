
## How to use API (v2)
Send a request to the follwing URLs:

|  Request (GET)              |                       Description                               |
| ---------------------------- | -------------------------------------------------------------- |
| http://localhost/v2/current     | Get all data from all the reportedly affected countries (List of Object) |
| http://localhost/v2/total  | Get the total numbers of Confirmed, Deaths, and Recovered |
| http://localhost/v2/confirmed   | Get the total number of Confirmed cases |
| http://localhost/v2/deaths | Get the total number of Deaths |
| http://localhost/v2/recovered | Get the total number of Recovered cases |
| http://localhost/v2/active | Get the total number of Active cases (Excluding Deaths and Recovered) |
| http://localhost/v2/country/china | Search a country by a key name (*space may be needed) |
| http://localhost/v2/country/kr | Search a country by an [ISO country code (alpha2)] (https://www.iban.com country-codes) |
| http://localhost/v2/timeseries/global |  Get the time series: global |
| http://localhost/v2/timeseries/{case} |  Get the time series: confirmed, deaths, recovered |
| http://localhost/v2/timeseries/US/{case} |  Get the time series (US): confirmed, deaths |

#### Examples API (v2)

1. Get current data
```json
http://localhost/v2/current
{"data": [{
      "location": "China",
      "confirmed": 81591,
      "deaths": 3281,
      "recovered": 73280,
      "active": 5030
    },
    {
      "location": "Italy",
      "confirmed": 69176,
      "deaths": 6820,
      "recovered": 8326,
      "active": 54030
    }.....n],
"dt": "2020-03-24 23:41:50",
"ts": 1585064510}
```

2. Get total data
```json
http://localhost/v2/total
{
  "data": {
    "confirmed": 417966,
    "deaths": 18615,
    "recovered": 107705,
    "active": 236306
  },
  "dt": "2020-03-24 23:41:50",
  "ts": 1585064510
}
```

3. Get confirmed cases
```json
http://localhost/v2/confirmed
{
  "data": 417966,
  "dt": "2020-03-24 23:41:50",
  "ts": 1585064510
}
```

4. Get deaths
```json
http://localhost/v2/deaths
{
  "data": 18615,
  "dt": "2020-03-24 23:41:50",
  "ts": 1585064510
}
```

5. Get recovered cases
```json
http://localhost/v2/recovered
{
  "data": 107705,
  "dt": "2020-03-24 23:41:50",
  "ts": 1585064510
}
```

6. Get active cases
```json
http://localhost/v2/recovered
{
  "data": 236306,
  "dt": "2020-03-24 23:41:50",
  "ts": 1585064510
}
```

7. Get a country data
```json
http://localhost/v2/country/th
{
  "data":{
    "location": "Thailand",
    "confirmed": 827,
    "deaths": 4,
    "recovered": 52,
    "active": 771
  },
  "dt": "2020-03-24 23:41:50",
  "ts": 1585064510
}

http://localhost/v2/country/united%20kingdom
{
  "data":{
    "location": "United Kingdom",
    "confirmed": 8164,
    "deaths": 423,
    "recovered": 140,
    "active": 7601
  },
  "dt": "2020-03-24 23:41:50",
  "ts": 1585064510
}
```

8. Get time series
```json
http://localhost/v2/timeseries/global
{
  "data": [
    {
      "1/22/20": {
        "confirmed": 555,
        "deaths": 17
      }
    },
    {
      "1/23/20": {
        "confirmed": 654,
        "deaths": 18
      }
    }...],
  "dt": "2020-03-25 23:37:49",
  "ts": 1585150669
}

http://localhost/v2/timeseries/confirmed
{
  "data": [
    {
      "Province/State": "",
      "Country/Region": "Afghanistan",
      "Coordinates": {
        "Lat": 33,
        "Long": 65
      },
      "TimeSeries": [
        {
          "date": "1/22/20",
          "value": 0
        },
        {
          "date": "1/23/20",
          "value": 0
        }...]
    }],
  "dt": "2020-03-25 23:37:49",
  "ts": 1585150669
```

9. Get time series (US)
```json
http://localhost/v2/timeseries/US/confirmed
{
  "data": [
    {"Province_State":"American Samoa",
    "Country_Region":"US",
    "Info":{
      "UID":16,
      "iso2":"AS",
      "iso3":"ASM",
      "code3":16,
      "FIPS":60.0,
      "Admin2":""
    },
    "Coordinates":{
      "Lat":-14.270999999999999,
      "Long":-170.132
    },
    "TimeSeries":[
      {"date":"1/22/20","value":0},
      {"date":"1/23/20","value":0},
      {"date":"1/24/20","value":0}]}, ...n],
  "dt":"2020-04-05 23:13:44",
  "ts":1586099624.0
}
```
