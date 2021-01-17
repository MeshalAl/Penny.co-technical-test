# Penny.co-technical-test

## about project:
### planned approach and outcomes:
####creation of modular spider interface
this was shot down pretty quick as structuring for modularity started to chew into time
use of only scrapy as main spider for most efficient processing (outcome: i really, REALLY wanted to make this work, however finding out that scrapy cannot run js code was soul crushing, and the need for splash requiring docker proved to add extra to the total file size, so a middleground was struck by using scrapy-selenium interface)
live-editing a excel file while keeping settings/formatting 
(outcome: generates new sheet with copied contents, this is pretty much due to inexperience and unfamiliarity with pandas and excel writers in general.)
knipex spider (outcome: this was actually the next part but times up, however it can be done by following this structure. ```request page via search with identifier> get target item url > get technical specs & images into a custom pipeline```, i remember trying to skip the javascript part (going full scrapy) entirely by creating custom request package as i couldn't figure out the correct structuring of the network payload 
## Installation & launching:
run `pip install -r requirements.txt`

to run, simply run the main.py, the results will be in (path_to_main.py)/Data/Source/ as results.xlsx.
