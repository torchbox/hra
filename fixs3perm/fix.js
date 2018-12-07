#!/usr/bin/env node
var AWS = require('aws-sdk');
var s3 = new AWS.S3();

var Bucket = 'trustsrv-io-hra-stage-tenant-mediabucket-13rpx7ditbzjf';
var Prefix = 'media/elearning/';

var acl = {
  "Owner": {
    "ID": "266da164c0f9db8887c13b3e84e1451e2bab6a031ef60037cbdd88eb5186daef"
  },
  "Grants": [
    {
      "Grantee": {
        "ID": "266da164c0f9db8887c13b3e84e1451e2bab6a031ef60037cbdd88eb5186daef",
        "Type": "CanonicalUser"
      },
      "Permission": "FULL_CONTROL"
    },
    {
      "Grantee": {
        "Type": "Group",
        "URI": "http://acs.amazonaws.com/groups/global/AllUsers"
      },
      "Permission": "READ"
    }
  ]
}



s3.listObjectsV2({Bucket, Prefix}, (err, data) => {
  if (err) {
    console.log(err);
    process.exit();
  } else {
    if (data.IsTruncated) {
      console.log('Data truncated - fix it!');
    } else {
      data.Contents.forEach((obj) => {
        s3.getObjectAcl({Bucket, Key: obj.Key}, (err, data) => {
          if (err) {
            console.log(err);
            process.exit();
          } else {
            //console.log(JSON.stringify(data, null, 2));
            s3.putObjectAcl({Bucket, Key: obj.Key, AccessControlPolicy: acl}, (err, data) => {
              if (err) {
                console.log(err, obj.Key);
              } else {
                console.log('ACL set: ', obj.Key);
              }
            })
          }
        })
      })
    }
  }
});
