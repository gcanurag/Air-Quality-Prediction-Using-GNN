import io
import csv
from locations import locations       # Import locations array from locations.py

def PredictionToSingleCSV(predictions):
    try:
        print("Processing predictions...")
       # print(predictions)
        print(len(predictions))
        print("You can see the predictions data above")

        csv_output = io.StringIO()
        # Create a CSV writer object
        csv_writer = csv.writer(csv_output)

        # Write header (pm2_5 and pm10)
        csv_writer.writerow(['pm2_5', 'pm10','location'])
        print(type(locations))
        print(len(locations))
        
        # Write prediction data, but only the first two values from each prediction
        for i,prediction in enumerate(predictions):        #enumerate used to iterate over a sequence while keeping track of both the index and the value.
            csv_writer.writerow(prediction[:2]+[locations[i]])  # Select only the first two values (pm2_5 and pm10)

            # Get the CSV string from memory
        csv_data = csv_output.getvalue()

        # Print the CSV data
       # print(csv_data)
        return csv_data 

        
        # Further processing can be done here.
    except Exception as e:
        print(f"Error in processing predictions: {e}")


