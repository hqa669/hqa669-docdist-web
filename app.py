from flask import Flask, render_template
import requests


def getHealthFacilityDirectory(url):
  response = requests.get(url)
  jdata = response.json()
  result = jdata["results"]
  selected = result[1:20]
  data = []
  for a in selected:
    address = a['address'] + ',' + a['city'] + ',' + a['state'] + ',' + a[
      'zip_code']
    facilityid = a['facility_id']
    facilityname = a['facility_name']
    phone = a['phone_number']
    data.append([facilityid, facilityname, address, phone])
  heading = ('Facility ID', 'Name', 'Address', 'Phone')
  return heading, data


def getHealthCareProvide(url):
  response = requests.get(url)
  jdata = response.json()
  result = jdata["results"]
  selected = result[1:20]
  data = []
  for a in selected:
    npi = a['npi']
    if not ['mid_nm'] == "":
      name = a['frst_nm'] + " " + a['mid_nm'] + " " + a['lst_nm']
    else:
      name = a['frst_nm'] + " " + a['lst_nm']
    address = a['adr_ln_1'] + "," + a['cty'] + "," + a['zip']
    org = a['org_nm']
    data.append([npi, name, org, address])
  heading = ('NPI', 'Name', 'Organization', 'Address')
  return heading, data


app = Flask(__name__)

url_healthfacility = 'https://data.cms.gov/provider-data/api/1/datastore/query/xubh-q36u/0?offset=0&count=true&results=true&schema=true&keys=true&format=json&rowIds=false'
heading_hf, data_hf = getHealthFacilityDirectory(url_healthfacility)

url_healthcareprovider = 'https://data.cms.gov/provider-data/api/1/datastore/query/mj5m-pzi6/0'

heading_hp,data_hp=getHealthCareProvide(url_healthcareprovider)
@app.route("/")
def display():
  return render_template('home.html', heading_hf=heading_hf, data_hf=data_hf,heading_hp=heading_hp,data_hp=data_hp)


if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)
