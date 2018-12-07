#!/bin/bash
export AWS_PROFILE=trustsrv-root
BUCKET=trustsrv-io-hra-tenant-mediabucket-ocsba082tcun
LOCAL_FOLDER=./files
REMOTE_PATH=media/elearning/
DRYRUN=--dryrun

#aws s3 ls $BUCKET

aws s3 sync --acl public-read $LOCAL_FOLDER s3://${BUCKET}/${REMOTE_PATH}
