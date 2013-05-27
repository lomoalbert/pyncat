pyncat
======

ncat -l 8086 --exec "ncat 127.0.0.1 8080" -k

======

python -m SimpleHTTPServer 8088 &

python pyncat.py -l 8086 -i 127.0.0.1 -p 8088 -k 100

