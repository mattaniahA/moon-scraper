# moon-scraper
download images from archives, compress to a reasonable size, find circles using opencv

## 1. download

### dl_main.py
bulk download source imgs from internet archive
`python3 -W ignore dl_main.py`
ignore since u wanna be sooo loud

## 1.5 reorg repo (chart plates only!) 
### nested_charts.sh

extract only the cute n sexy images 
`./nested_charts.sh`




## 2. fix res

### compress_img.sh
iterate through img directory and compress images
`./resolution_scripts/compress_img.sh`

### compress_img_nest.sh
iterate through img directory (WITH NESTED FOLDERS) and compress images
this will maintain the file structure
`./resolution_scripts/compress_img_nest.sh`




## 3. crop

### autocrop_opencv.py
auto crop + center moon for solar eclipse imgs 
`python3 autocrop_opencv.py`


### nested_charts.sh
iterate through img directory (WITH NESTED FOLDERS) and compress images
this will maintain the file structure
`./nested_charts.sh`



# earth orientation parametersss
### eop/interpret_eop.py
given a date, find and print the closest represented EOP data from JSON 


