# WebSpider (Scrapy)

Pajączek internetowy wyciągający artykuły z serwisu trójmiasto.pl.

Instalacja:

```bash
pip install Scrapy
pip install beautifulsoup4
```

Uruchomienie scrapy w trybie konsoli

```bash
scrapy shell 'https://trojmiasto.pl/'
```

Uruchomienie

```bash
scrapy crawl trojmiasto -o output.json
```
