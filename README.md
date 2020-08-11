# Farmer Insights
Help farmers reduce water usage for Grown Crops
[Submission Video](https://ibm.box.com/s/tanox61eg1qq58g7y1tmxm47o9tp86ij)

## Motivation
Water sustainability is vital. Water is a finite and irreplaceable resource that we as a society need to conserve. Farmers are especially guilty of overuse. Having a way that could accurately utilize weather data and provide a personalized and optimized watering schedule for farmers would be exceedingly helpful in minimizing waste. Our technology could be paired with additional sensors, such as soil sensors, to make even more targeted irrigation schedules.


In recent years there has been an increase in droughts across the globe. This has impacted communities by increasing water shortages, increasing risk of fires, and reduced crop yield. Agriculture can account for 60-75% of global water withdrawals. Irrigation helps to provide a supply to plants to maximize crop yield. Irrigation can be inefficient due to over watering crops and depleting resources. Irrigation systems that include a pump system need a constant supply in order to maintain pressure. This is causing a severe impact in aquifers. The fresh water is being pulled to over water crops and salt water is replacing the reserve. Irrigation controls to reduce water usage surrounding rainfall events can reduce water waste, and that's what we aim to do.


Using this tool, small and medium sized farmers will be able to better understand their water usage and follow precipitation insights to reduce water used in irrigation. Efficient irrigation usage can show a 35% reduction in water usage over a season. For a farm of 5 acres this can account for x reduction in gallons of water used. The recommendations of when to reduce irrigation and by how much allow crops to receive adequate water supplies and produce a maximum yield.


## Features

### Recommended Irrigation Scheduling Based on Rainfall Data
Based on rainfall data for the day and the original irrigation schedule for a dry day, our app would recommend the irrigation frequency and length of irrigation for the day to minimize water usage on the farm

### Interactive Watson Chatbot Experience
Don't know how to use the website? Ask the chatbot! This is useful as an option for less tech-savvy farmers to understand how to use the service.

### Daily Precipitation Rate Display Every 15 Minutes
Using a GET request to another page on the site, Weather Company data about the next seven hours of rainfall is transformed into a graph, which lets the users easily view the rain forecast for the day.

### Suggestions on When to Avoid Irrigation
The Home tab performs a GET request to another page on the site, which uses the Weather Company's API to get the day's forecast. From that data, it finds any amount of rainfall over zero, and is able to advise the user on what time periods they can expect it to rain, and therefore when to avoid irrigating

## How to run
1. Clone the repo
2. In the root directory of the project, run `pip3 install -r requirements.txt`
3. Initialize the server by running `python3 server.py`
4. Open up `localhost:5000` in your browser. (Works best in Google Chrome)
5. You can register your own account or login using the account `corn_grower` with the password `password` to see an account that's pre-populated with data