CFLAGS=-g -Wall -pedantic -std=c99
OUTFILE=os2drive
INSTALL_DESTINATION=/usr/local/bin

default:
	gcc $(CFLAGS) OS2Drive.c -lssl -lcrypto -o $(OUTFILE)

clean:
	rm $(OUTFILE)

install:
	make default
	-cp $(OUTFILE) $(INSTALL_DESTINATION)
	-chmod +x $(INSTALL_DESTINATION)/$(OUTFILE)
	echo "Done!!!"
