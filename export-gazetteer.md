## (Mac OS X)

1. Install [mdbtools](https://github.com/brianb/mdbtools)

	# pre-req: glib 2.0
	brew install glib

	mkdir ~/projects/mdbtools
	cd ~/projects/mdbtools
	wget https://github.com/brianb/mdbtools/archive/0.7.1.tar.gz
	tar xvf 0.7.1.tar.gz
	cd mdbtools-0.7.1
	autoreconf -i -f
	./configure --disable-man
	make

2. Extract data

Documentation for mdb-sql is [here](https://github.com/brianb/mdbtools/blob/master/doc/mdb-sql.txt).

    ./mdb-sql -p -F -o suburbs.csv ~/projects/postcodes/scratch/gazetteer_2012.mdb

    ```sql
    select name, state_id, postcode, latitude, longitude, variant_name, status from tblmain where feat_code = 'SUB'
    go
    ```