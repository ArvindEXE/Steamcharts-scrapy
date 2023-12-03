# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter 
        

class SteamchartsPipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        ## Change average player count to interger
        avg_player_string = adapter.get('Avg_players')
        avg_player_string_int = int(round(float(avg_player_string)))
        adapter['Avg_players'] = avg_player_string_int

        ## Change gain to float value
        gain_keys = ['Gain', 'Gain_percentage']
        for gain_key in gain_keys:
            value = adapter.get(gain_key)
            value = value.strip('%')
            if value == '-':
                value = float(0)
            else:
                value = float(value)
            adapter[gain_key] = float(value)

        ## Format 'month' column to 'YYYY-MM-DD' format
        date_string = adapter.get('Month')
        date_string = date_string.split(" ")
        format_string = ""
        
        if date_string[0] == 'January':            
            format_string = date_string[1] + '-01' + '-31'
            date_index = 1
        elif date_string[0] == 'February':                        
            format_string = date_string[1] + '-02' + '-28'
            date_index = 2
        elif date_string[0] == 'March':                          
            format_string = date_string[1] + '-03' + '-31'
            date_index = 3            
        elif date_string[0] == 'April':                          
            format_string = date_string[1] + '-04' + '-30'
            date_index = 4               
        elif date_string[0] == 'May':                          
            format_string = date_string[1] + '-05' + '-31'
            date_index = 5               
        elif date_string[0] == 'June':                          
            format_string = date_string[1] + '-06' + '-30'
            date_index = 6               
        elif date_string[0] == 'July':                          
            format_string = date_string[1] + '-07' + '-30'
            date_index = 7               
        elif date_string[0] == 'August':                          
            format_string = date_string[1] + '-08' + '-31'
            date_index = 8               
        elif date_string[0] == 'September':                          
            format_string = date_string[1] + '-09' + '-30'
            date_index = 9               
        elif date_string[0] == 'October':                        
            format_string = date_string[1] + '-10' + '-31'
            date_index = 10               
        elif date_string[0] == 'November':         
            format_string = date_string[1] + '-11' + '-30'
            date_index = 11               
        elif date_string[0] == 'December':
            format_string = date_string[1] + '-12' + '-31'
            date_index = 0             
        else:
            format_string = 'last 30 days'
                                   
        adapter['Month'] = str(format_string)

        return item