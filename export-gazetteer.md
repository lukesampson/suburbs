## (Mac OS X)

1. Download Gazetteer of Australia 2012 from [here](https://www.ga.gov.au/products/servlet/controller?event=GEOCAT_DETAILS&catno=76695)

2. Extract the mdb it contains to data/gazetteer2012.mdb

3. Install [mdbtools](https://github.com/brianb/mdbtools)

	brew install mdbtools

4. Extract data

Documentation for mdb-sql is [here](https://github.com/brianb/mdbtools/blob/master/doc/mdb-sql.txt).

    mdb-sql -p -F -o data/gazetteer2012_suburbs.csv scratch/gazetteer2012.mdb

    ```sql
    select name, state_id, postcode, latitude, longitude, variant_name, status from tblmain where feat_code = 'SUB'
    go
    ```