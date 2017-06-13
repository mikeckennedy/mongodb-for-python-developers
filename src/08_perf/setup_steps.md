This section on performance is best performed with a large database of cars and owners.

There is a load_data part of the app which will generate this database but it will take a long time (30 minutes or something like this).

To make things faster, I have included a DB which can be imported in `REPO/data/dealership_db_250k.zip`

To use this database, you simple need to unzip and then restore it with the following command:

In the terminal / command line change into the extracted folder containing the `*.bson` and `*.json`, then type:

`mongorestore --drop --db dealership ./`

On Windows, use `.\` rather than `./`

Now you should have a dealership db in MongoDB. Be sure to check the indexes. You may need to drop them (other than `_id` indexes).

