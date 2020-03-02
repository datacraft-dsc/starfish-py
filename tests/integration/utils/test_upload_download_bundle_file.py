"""


Test bundle file upload/download


"""

import hashlib
import tempfile
import secrets

from starfish.utils.data_bundle import (
    decode_readable_size,
    register_upload_bundle_file,
    download_bundle_file
)

TEST_FILE_SIZE = '120mb'

def test_bundle_file_upload_download(remote_agent):
    # create temp large file
    max_size = decode_readable_size(TEST_FILE_SIZE)
    size = 0
    with tempfile.NamedTemporaryFile() as fp:
        md5sum = hashlib.md5()
        while size < max_size:
            data = secrets.token_bytes(1024 * 100)
            size += len(data)
            fp.write(data)
            md5sum.update(data)

        test_data_md5 = md5sum.hexdigest()
        fp.seek(0)
        filename = fp.name
        asset_bundle = register_upload_bundle_file(remote_agent, filename)

        fp.seek(0)

        with tempfile.NamedTemporaryFile() as out_fp:
            download_size = download_bundle_file(remote_agent, asset_bundle, out_fp.name)
            out_fp.seek(0)
            assert(download_size == size)
            md5sum = hashlib.md5()
            while True:
                data = out_fp.read(1024 * 100)
                if data:
                    md5sum.update(data)
                else:
                    break

            assert(test_data_md5 == md5sum.hexdigest())
