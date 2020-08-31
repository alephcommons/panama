all: fetch install parse

fetch:
	mkdir -p data
	wget -c -P data/ https://archive.org/download/records-000001-050000.tar/records-000001-050000.tar.bz2
	wget -c -P data/ https://archive.org/download/records-000001-050000.tar/records-100000-150000.tar.bz2
	wget -c -P data/ https://archive.org/download/records-000001-050000.tar/records-150000-200000.tar.bz2
	wget -c -P data/ https://archive.org/download/records-000001-050000.tar/records-200000-250000.tar.bz2
	wget -c -P data/ https://archive.org/download/records-000001-050000.tar/records-250000-300000.tar.bz2
	wget -c -P data/ https://archive.org/download/records-000001-050000.tar/records-300000-350000.tar.bz2
	wget -c -P data/ https://archive.org/download/records-000001-050000.tar/records-350000-400000.tar.bz2
	wget -c -P data/ https://archive.org/download/records-000001-050000.tar/records-400000-450000.tar.bz2
	wget -c -P data/ https://archive.org/download/records-000001-050000.tar/records-450000-500000.tar.bz2
	wget -c -P data/ https://archive.org/download/records-000001-050000.tar/records-50000-100000.tar.bz2
	wget -c -P data/ https://archive.org/download/records-000001-050000.tar/records-500000-550000.tar.bz2
	wget -c -P data/ https://archive.org/download/records-000001-050000.tar/records-550000-600000.tar.bz2
	wget -c -P data/ https://archive.org/download/records-000001-050000.tar/records-600000-619300.tzr.bz2
	wget -c -P data/ https://archive.org/download/records-000001-050000.tar/records-650000-700000.tar.bz2
	wget -c -P data/ https://archive.org/download/records-000001-050000.tar/records_645000-650000.tar.bz2

install:
	pip install followthemoney followthemoney-store banal normality lxml

parse:
	python parse.py