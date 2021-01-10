#!/bin/bash
TIME=`date +%b-%d-%y`                      # This Command will read the date.

# To backup directories
# FILENAME=backup-pickndell_db-$TIME.tar.gz       # The filename including the date.
# SRCDIR=/data/dnd_sos                            # Source backup folder.
# DESDIR=/data/backup                             # Destination of backup file.
# tar -cpzf $DESDIR/$FILENAME $SRCDIR

/usr/bin/pg_dump bingo_db > /home/ubuntu/backup/bingo_db-$(date +\%F).db