# -*- encoding: utf-8 -*-

import requests
import urlparse
from lxml.html import document_fromstring
import shapely.geometry

from app.model import db, Listing
from app.common import flask_app_context


LISTING_SEARCH_IMMO_BORDEAUX_URL = 'http://www.stephaneplazaimmobilier.com/ville_bien/33000+Bordeaux_1/33000-bordeaux.html'
LISTING_SEARCH_IMMO_PARIS_URL = 'http://www.stephaneplazaimmobilier.com/catalog/result_carto.php?action=update_search&map_polygone=&C_28_search=EGAL&C_28_type=UNIQUE&C_28=Location&C_65_search=CONTIENT&C_65_type=TEXT&C_65=75+PARIS&C_65_autocomplete=75+PARIS'


class ScrapingError(Exception):
    pass


def parse_listing_item(listing_url):
    """Parse a single item and maybe add it to the db"""

    print "[*] Parsing listing item: {}".format(listing_url)

    item_page = requests.get(listing_url)
    item_doc = document_fromstring(item_page.content)

    r = item_doc.xpath(u'//*[@id="item-infos"]/div/div[1]/div/h1/span[@class="item-infos"]/text()')
    if len(r) < 1:
        raise ScrapingError('Expected a name')
    item_name = ' '.join(''.join(r).split())

    r = item_doc.xpath(u'//*[@id="criteres_bien"]/div[contains(@class, "General")]/div/ul/li/div/div[.="Type de bien"]/../div[2]/b/text()')
    if len(r) != 1:
        raise ScrapingError('Expected a type of listing')
    if r[0] == 'Appartement':
        item_type = 'apartment'
    elif r[0] == 'Immeuble':
        item_type = 'building'
    elif r[0] == 'Maison':
        item_type = 'house'
    #NOTE: Not found yet:
    elif r[0] == 'Stationnement':
        item_type = 'parking'
    else:
        item_type = 'land'

    rent_found = False
    r = item_doc.xpath(u'//*[@id="criteres_bien"]/div[contains(@class, "aspects_financiers")]/div/ul/li/div/div[.="Prix"]/../div[2]/b/text()')
    rent_found = len(r) == 1
    if not rent_found:
        r = item_doc.xpath(u'//*[@id="criteres_bien"]/div[contains(@class, "aspects_financiers")]/div/ul/li/div/div[.="Loyer charges comprises"]/../div[2]/b/text()')
        rent_found = len(r) == 1
    if not rent_found:
        raise ScrapingError('Expected a price/rent')

    item_rent = int(r[0].split()[0])

    r = item_doc.xpath(u'//*[@id="criteres_bien"]/div[contains(@class, "surfaces")]/div/ul/li/div/div[.="Surface"]/../div[2]/b/text()')
    if len(r) != 1:
        raise ScrapingError('Expected a surface area')
    item_surface_area = float(r[0].split()[0])

    r = item_doc.xpath(u'//*[@id="criteres_bien"]/div[contains(@class, "interieur")]/div/ul/li/div/div[.="Nombre pièces"]/../div[2]/b/text()')
    if len(r) != 1:
        raise ScrapingError('Expected a room count')
    item_room_count = int(r[0])

    r = item_doc.xpath(u'//div[@id="roadmap"]/div[@id="gmap"]')
    if len(r) != 1:
        raise ScrapingError('Expected a google map element')
    item_lng = float(r[0].get('data-lng'))
    item_lat = float(r[0].get('data-lat'))
    item_geometry = shapely.geometry.point.Point(item_lng, item_lat).wkt

    # NOTE: I do not think that name/type are sufficient to correctly identify a specific item.

    there_s_change = False
    row = db.session.query(Listing).filter_by(name=item_name, listing_type=item_type).one_or_none()
    if row is None:
        print "[#] New item"
        listing_item = Listing(
            name=item_name,
            url=listing_url,
            geometry=item_geometry,
            listing_type=item_type,
            surface_area=item_surface_area,
            room_count=item_room_count,
            rent=item_rent,
            is_furnished=False
        )
        db.session.add(listing_item)
        there_s_change = True
    else:
        print "[!] Item already existing"
        #TODO: update ?
        pass

    return there_s_change


def parse_listing(listing_search_url=LISTING_SEARCH_IMMO_PARIS_URL):
    """Parsing a listing of items from a specific search query"""

    listing_page = requests.get(listing_search_url)
    listing_doc = document_fromstring(listing_page.content)
    listing_base_url = listing_doc.base

    r = listing_doc.xpath(u'//div[@id="result_carto_listing"]')
    if len(r) != 1:
        raise ScrapingError('Expected one listing of items')
    listing_items = r[0]

    listing_items = listing_items.xpath(u'//div[@class="row-fluid"]/div[1]/a/@href')
    if len(r) < 1:
        raise ScrapingError('Expected at least one item')

    with flask_app_context:
        there_s_change = False

        for item_sublink in listing_items:
            listing_url = urlparse.urljoin(listing_base_url, '.' + item_sublink)
            there_s_change |= parse_listing_item(listing_url)

        if there_s_change:
            print "[+] Committing ..."
            db.session.commit()
        else:
            print "[-] Nothing to commit !"


parse_listing()
