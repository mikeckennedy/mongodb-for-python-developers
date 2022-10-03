# Directions to restore this data into MongoDB

To restore any of these databases to MongoDB, you'll need to uncompress them and then run this command:

```
mongorestore --drop --db DATABASE /path/to/unziped/dir
```

If you are using an authenticated connection on another server, this more verbose version is required:

```
mongorestore -u admin -p <mypassword> --authenticationDatabase 'admin' --ssl --host <my_hostname> --sslCAFile mongod.crt --sslPEMKeyFile mongod.pem --drop --db DATABASE /path/to/unziped/dir
```

Note this references this two MongoDB certifications for connecting. You can alternatively use the `--sslAllowInvalidCertificates` flag to ignore them.
