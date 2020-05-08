#!/usr/bin/env python3

import argparse
import hashlib

# This script reads the --value argument from the command
# line and outputs its SHA 512 hash.
# In this tutorial, we use this for generating the value
# that the application uses for its basic authentication.
# We do this, so the basic auth secret is not stored in
# raw format on Google Cloud Run, which could impose a
# security risk.

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--value', help='The value to hash', required=True)

    args = parser.parse_args()

    if (not args.value.strip()):
        raise ValueError("--value argument can't be blank!")

    hash_object = hashlib.sha512(bytearray(args.value, encoding='utf8'))
    hashed = hash_object.hexdigest()

    print(hashed)
