"""
    Asset class to handle core imutable asset and it's metadata


"""


class Asset():
    """

    :param dict metadata: metadata for the asset
    :param did: Octional did of the asset, if the asset is new then the did will be None.
    :type did: None or str

    """
    def __init__(self, metadata, did=None):
        """
        init an asset class
        """
        self._metadata = metadata
        self._did = did

    def set_did(self, did):
        """
        This method makes the object immutable.
        So maybe a solution is that we have a 'copy' and
        set the did in the __init__ of the new class, to return a mutable copy of the
        same asset object.
        """
        self._did = did

    @property
    def did(self):
        """
        :return: the asset did
        :type: str
        """
        return self._did

    @property
    def metadata(self):
        """
        :return: The metadata for this asset
        :type: dict
        """
        return self._metadata

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
