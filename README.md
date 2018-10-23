

# Housing Market
This is a dummy project that aims to build an API that enables users to navigate the rental market.

The API should be able to work properly in Bordeaux:
* Contextual information can be retrieved from OpenStreetMap, Bordeaux's open data websites and any other sources you see fit.
* Rental listings can be scraped from various websites such as leboncoin.fr or seloger.com.
# Usage
With Docker:
1. `docker-compose up`
2. copy this URL into your web browser: http://admin:default@127.0.0.1:9999/listings

Without Docker:

1. `virtualenv env`
2. `source env/bin/activate`
3. `pip install pip setuptools --upgrade`
4. `pip install -r requirements.txt`
5. `python setup.py develop`
6. `python app/common/init_db.py`
7. `python app/api.py`

# Contribution
If you want to see your modifications, use `docker-compose up --force-recreate --build`.

# ToDo
1. Make sure `/listings:search` returns results as specified in the `swagger.yml` file.
2. Add `tram_stop` and `bus_stop` to the amenities (datasets are available on the [open data website](https://data.bordeaux-metropole.fr/themes))
3. Make sure `Listing` table is refreshed every 15 minutes (remove no longer available listings and add new ones)
4. Store user's most recent search and send them an email notification when a new listing that matches their search criteria appears.
