grow_motion
===========
take a picture of the plants current state and take moisture and temperature readings

Setup
=====
You need::

    opencv2, sqlalchemy, postgresql, psycopg2, alembic

Ive configured the `/etc/postgresql/9.4/main/pg_hba.conf` file as::

    local   all             postgres                                peer
    local   all             all                                     peer
    host    all             all             127.0.0.1/32            md5
    host    all             all             ::1/128                 md5
    local all postgres ident

After these are setup and you can import and use the stuff inside set up your tables::

    $ > alembic upgrade head

Usage
=====
Usage assumes this line is executed before each command::

    export $PYTHONPATH='/home/pi/projects/grow_motion/'

Data harvest
------------
Run the command::

    nohup python -u ~/projects/grow_motion/main.py >>/var/log/snn/grower.log 2>/var/log/snn/grower.err &

and watch your data flow in :)

Images to Html5 video converter
-------------------------------

Simply::

    python img_to_mp4.py
