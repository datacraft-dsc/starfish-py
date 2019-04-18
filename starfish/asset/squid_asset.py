"""
    Squid Asset
"""

from starfish.asset.asset_base import AssetBase

class SquidAsset(AssetBase):
    """

    Create a new squid asset to use in the Ocean network

    :param metadata: metadata to store for this asset, it must be a valid squid metadata dict
    :type metadata: dict
    :param did: did of the asset if it is registered, can be None for a new non registered asset
    :type did: None or str

    """

    @staticmethod
    def generate_metadata():
        """
        Return a generated example metadata that can be changed by the child asset class

        :return: default metadata
        :type: dict
        """
        metadata = {
            'name': "Ocean protocol white paper",
            'type': "dataset",
            'description': "Introduce the main concepts and vision behind ocean protocol",
            'size': "1mb",
            'dateCreated': "2012-10-10T17:00:000Z",
            'author': "Ocean Protocol Foundation Ltd.",
            'license': "CC-BY",
            'copyrightHolder': "Ocean Protocol Foundation Ltd.",
            'encoding': "UTF-8",
            'compression': "",
            'contentType': "text/csv",
            'workExample': "Text PDF",
            'inLanguage': "en",
            'categories': ["white-papers"],
            'tags': "data exchange sharing curation bonding curve",
            'price': 23,
            'files': [
                {
                    "url": "https://testocnfiles.blob.core.windows.net/testfiles/testzkp.pdf",
                    "checksum": "efb2c764274b745f5fc37f97c6b0e761",
                    "checksumType": "MD5",
                    "contentLength": "4535431",
                    "resourceId": "access-log2018-02-13-15-17-29-18386C502CAEA932"
                },
                {
                    "url": "s3://ocean-test-osmosis-data-plugin-dataseeding-1537375953/data.txt",
                    "checksum": "efb2c764274b745f5fc37f97c6b0e761",
                    "contentLength": "4535431",
                    "resourceId": "access-log2018-02-13-15-17-29-18386C502CAEA932"
                },
                {
                    "url": "http://www3.cs.stonybrook.edu/~algorith/implement/graphbase/distrib/cweb3"
                     ".4e.tar.gz"
                },
            ],
            'links': [
                {
                    "sample1": "http://data.ceda.ac.uk/badc/ukcp09/data/gridded-land-obs/gridded-land"
                    "-obs-daily/",
                },
                {
                    "sample2": "http://data.ceda.ac.uk/badc/ukcp09/data/gridded-land-obs/gridded-land"
                    "-obs-averages-25km/",
                },
                {
                    "fieldsDescription": "http://data.ceda.ac.uk/badc/ukcp09/",
                },
            ],
        }
        return metadata
