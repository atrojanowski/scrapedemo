# scrapedemo
A quick demo for scraping several investment websites.  Creating a flask webservice with REST api is out of scope for "free sample".  Also, unsure what is meant by "extract the domain" (isn't that already being done?). 

In order to run this demo, execute the script via python from the command line:

```$ python multiscraper.py```

The requested output is sent to STDOUT and looks like:
```
=================
Requested Output:
{
  "amplifypartners.com": [
    "actioniq.com",
    "anchorage.com",
    ...
    "usefulsensors.com",
    "yeshid.com"
  ],
  "lsvp.com": [
    "udaan.com",
    "rubrik.com",
    ...
    "moveworks.ai",
    "quantumscape.com"
  ]
}        
```


## Assumptions
This project assumes 
- that the user has python installed.
- that the user has scrapy installed.  If not installed, use:

    ```$ pip install scrapy``` 

- that the websites to be scraped have not updated significantly since the demo was written.
- that the script is executed from somewhere that has network access to the requested urls.
- that I fully understood the public/aquired/active requirement (for the amplifypartners I matched "active" and for lsvp I matched not "public"/"acquired")

## Architecture
This is a single file project so there is no architecture to speak of: a single python script file and this README.

## Data Structures
The scraped domains are stored in a simple Python dictionary as this is the requested output.

The dictionary is a dict-of-lists where the key to the dict is the base url (only domain and extension) of the page to be scraped and the list is a list of the domains which have an acceptable status.

## Testing Methodology
If this was an actual packaged project, there would be a sample of each website included to run local unit tests on (or a fixture).

This project was tested using an official python docker image (python:3.11-bullseye) with the only material change being the installation of scrapy (from assumptions).