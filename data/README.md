# Directions to restore this data into MongoDB

To restore any of these databases to MongoDB, you'll need to uncompress them and then run this command:

```
mongorestore --drop --db DATABASE /path/to/unziped/dir
```