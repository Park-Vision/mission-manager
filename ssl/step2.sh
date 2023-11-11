#!/usr/bin/bash
openssl pkcs8 -in client_drone_client.key -topk8 -v1 PBE-SHA1-3DES -out client_drone_client_v2.key
