echo IMPORTING COLLECTION
mkdir "/tmp/flowers"
tar -xzvf /docker-entrypoint-initdb.d/flowers.tar.gz --directory /tmp/flowers
mongoimport --authenticationDatabase=admin --username=$MONGO_INITDB_ROOT_USERNAME --password=$MONGO_INITDB_ROOT_PASSWORD --db=flowers --collection=flower --file=/tmp/flowers/flower.json
mongoimport --authenticationDatabase=admin --username=$MONGO_INITDB_ROOT_USERNAME --password=$MONGO_INITDB_ROOT_PASSWORD --db=flowers --collection=flower_classes --file=/tmp/flowers/flower_classes.json
mongoimport --authenticationDatabase=admin --username=$MONGO_INITDB_ROOT_USERNAME --password=$MONGO_INITDB_ROOT_PASSWORD --db=flowers --collection=fs.files --file=/tmp/flowers/fs.files.json
mongoimport --authenticationDatabase=admin --username=$MONGO_INITDB_ROOT_USERNAME --password=$MONGO_INITDB_ROOT_PASSWORD --db=flowers --collection=fs.chunks --file=/tmp/flowers/fs.chunks.json
echo "CLEANING UP"
rm -r /tmp/flowers
echo DONE IMPORTING
