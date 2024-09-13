If you want to run it localy use their github repo
* https://github.com/mbloch/mapshaper

-- there are some useful code that you are able to use after loading your map
* filtering the area:

```text
 -filter 'LSOA21NM.startsWith("Swansea") || LSOA21NM.startsWith("Neath Port Talbot")'
```

```text
 mapshaper -o -proj wgs84
```
