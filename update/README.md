
This repo contains Python 2.7 codes for updating the existing RLK MySQL DB
with new data from BMI.  Major actions of the code are to: 

    retrieve information and data points from a new BMI DB;

    convert BMI information to RLK data and metadata;

    filter and retain only the important datasets;

    update or introduce new data to the RLK MySQL DB.


To run:

Run Python script bmi_2_rlk_SQL.py + list the BMI database names in the command line
in chronologically asending order.  The location of the databases is set in load_bmi() 
within bmi_2_rlk_SQL.py.
For example,

    python  bmi_2_rlk_SQL.py  01_03_2014.xlsm 01_05_2014.xlsm [...] 01_mm_20yy.xlsm


Dependencies:

    MySQLdb  - python implementation of MySQL queries

    openpyxl - for reading BMI .xlsm DB


The files in this package are:

    bmi_2_rlk_SQL.py: 
    Contains bmi_update(), the main loop code carrying out all of the actions above.

    rlk_mysql.py: 
    Functions for interactions with RLK database.  Also, currently includes codes for
    dataset title filtering and the counting tools (i.e., class Sheet_info) for verification 
    sheet-by-sheet of the numbers of titles: kept (past filter), new, replaced, discard.  
    These will eventually be moved to their own separate files.

    bmi_get_update:  
    Contains the class 'BMI_Info' which extracts info from the BMI database and 
    puts it into a useable form.

    unit_tests.py:
    Set of unit tests covering most methods.

    currency_list.dat:
    Python list data pickle containing ISO country codes for eliminating titles expressed in 
    currency that is anything other than US$.  This should be kept update-to-date as country codes 
    change.

    verify_update.py:
    Code that goes through every dataset in the BMI DB and checks that each data point is correctly 
    inserted into the MySQL DB.


Future fixes & optimizations:

    Fix titles with currency by ISO country code.  These are being cleaned out to some extent, but have not 
    tested how much.

    In previous version of the BMI update code, the country string was as follows:
    country = get_col[1].sub(",","(") country = country.sub("of","of)").
    Is this still needed?

    Instead of INSERT, use REPLACE for updating chart1.  Acts just like insert unless having 
    same value of primary key in which case it replaces current data.
    
    Fix the ‘counter’ part of the code - messy for the moment, and not completely correct:
        
        add_it_up(): jnk_* tables should not be hard-coded;

        add_it_up(): the get_last_id() calls should be used as the starting id's for the next iteration
        in the main loop;
        
        eliminate the use of add_it_up() function altogether by tidying up the class Sheet_Info and 
        instantiating directly in the code;

    Migrate the functions for the title cleaning to another file.

    Move class Sheet_Info to its own file.

    Fix the ‘counter’ part of the code:

    
        within add_it_up(), jnk_* tables should not be hard-coded

        eliminate the use of add_it_up() function altogether by tidying up the class Sheet_Info and 
        instantiating directly in the code.


Typical sources of error running verify_update.py:

    Data replication:
    Many datasets in the BMI DB are repeated on different sheets with similar data.  The duplicate dataset maybe 
    rounded or can span different years if '0.' occupies the trailing year data values. 

    Title replication:
    The same title may be used to represent a dataset and a derived quantity of that data set.  For example,
    The percent year-on-year value (% y-o-y) can hold the same title.  These derivative values, so far, appear to 
    come only after the actual dataset, and since the code captures data only once, no modifications occur in this 
    case.

