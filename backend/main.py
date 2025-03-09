from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import torch
import io
import pickle
from torch_geometric.data import Data
from sklearn.preprocessing import StandardScaler
from pydantic import BaseModel
from model import TemporalEdgeWeightModule, SpatioTemporalGNN
import json
import pandas as pd
from graph_utils import create_graph_from_csv  # Import your function
from PredictionToSingleCSV import PredictionToSingleCSV   # Importing the PredictionToSingleCSV file for converting to CSV file.
from fastapi.responses import StreamingResponse



# Set the device (use GPU if available, otherwise use CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load the saved scalers
with open("scalers/x_scaler.pkl", "rb") as f:
    x_scaler = pickle.load(f)
with open("scalers/edge_attr_scaler.pkl", "rb") as f:
    edge_attr_scaler = pickle.load(f)

# # Load the saved model checkpoint
# checkpoint_path = "TemporalGNN.pth"
# checkpoint = torch.load(checkpoint_path, map_location=device)

# # Inspect the checkpoint keys
# print("Checkpoint keys:", checkpoint["model_state_dict"].keys())



# # Infer input features
# if "gat.lin_src.weight" in checkpoint["model_state_dict"]:
#     in_features = checkpoint["model_state_dict"]["gat.lin_src.weight"].shape[1]
# elif "gat.lin.weight" in checkpoint["model_state_dict"]:
#     in_features = checkpoint["model_state_dict"]["gat.lin.weight"].shape[1]
# else:
#     raise KeyError("Could not find GATConv weight parameter in checkpoint.")

# out_features = checkpoint["model_state_dict"]["fc_out.weight"].shape[0]
# edge_dim = checkpoint["model_state_dict"]["gat.lin_edge.weight"].shape[1]

# # Initialize the model
# model = SpatioTemporalGNN(in_features, hidden_dim=64, out_channels=out_features, edge_dim=edge_dim).to(device)
# model.load_state_dict(checkpoint["model_state_dict"])
# model.eval()  # Set the model to evaluation mode

# # Initialize edge memory
# edge_memory = checkpoint["edge_memory"].to(device)

# Load the saved model checkpoint
checkpoint_path = "TemporalGNN.pth"
checkpoint = torch.load(checkpoint_path, map_location=device)

in_features = 4  # Set this to match the checkpoint
out_features = checkpoint["model_state_dict"]["fc_out.weight"].shape[0]
edge_dim = checkpoint["model_state_dict"]["gat1.lin_edge.weight"].shape[1]

# Initialize the model
model = SpatioTemporalGNN(in_features, hidden_dim=64, out_channels=out_features, edge_dim=edge_dim).to(device)
model.load_state_dict(checkpoint["model_state_dict"])
model.eval()  # Set the model to evaluation mode

# Initialize edge memory
edge_memory = checkpoint["edge_memory"].to(device)











# Define a Pydantic model for input validation
class InferenceInput(BaseModel):
    x: list  # Node features
    edge_index: list  # Edge indices
    edge_attr: list  # Edge attributes



app = FastAPI()


# Enable CORS for Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)





# Helper function to perform prediction
def perform_prediction(x, edge_index, edge_attr):
    try:
        # print(json.dumps(data, indent=4))
        # Convert input data to tensors
        x = torch.tensor(x, dtype=torch.float).to(device)
        edge_index = torch.tensor(edge_index, dtype=torch.long).to(device)
        edge_attr = torch.tensor(edge_attr, dtype=torch.float).to(device)

        # Reshape edge_attr if necessary
        if edge_attr.dim() == 1:
            edge_attr = edge_attr.view(-1, 1)

        # Normalize input data using the saved scalers
        x = torch.tensor(x_scaler.transform(x.cpu().numpy()), dtype=torch.float).to(device)
        edge_attr = torch.tensor(edge_attr_scaler.transform(edge_attr.cpu().numpy()), dtype=torch.float).to(device)

        # Create a PyG Data object
        data = Data(x=x, edge_index=edge_index, edge_attr=edge_attr)

        # Perform inference
        with torch.no_grad():
            y_pred, _, _ = model(data.x, data.edge_index, data.edge_attr, edge_memory)

        # Inverse transform the predictions to original scale
        y_pred = x_scaler.inverse_transform(y_pred.cpu().numpy())

        print("prediction made")
        return  y_pred.tolist()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





# POST endpoint to accept data and make predictions
@app.post("/predict")
def predict(input_data: InferenceInput):
     return perform_prediction(input_data.dict())  # Perform prediction and return results 


@app.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...)):
    try:
        # Read file directly from memory into a Pandas DataFrame
        content = await file.read()
        df = pd.read_csv(io.StringIO(content.decode("utf-8")))



        # Print the first five rows in the backend terminal
        print("CSV File Contents (First 5 Rows):")
        print(df.head())



        x, edge_index, edge_attr = create_graph_from_csv(df)
        # print("Graph received!!",graph_data)
        print("Graph received!!")
        print(edge_index)
        
        y_prediction=perform_prediction(x, edge_index, edge_attr)
        if y_prediction:
            print("Prediction Received!!")
        

        print("predictionn completed")
        CSV=PredictionToSingleCSV(y_prediction)  # Passing the prediction results into PredictionTOCSV function.
        print(CSV)
        if not CSV:
            raise HTTPException(status_code=500, detail="Failed to generate CSV data")
        
        print("Response CSV Data:", CSV)
        return StreamingResponse(
            io.StringIO(CSV),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=predictions.csv"}
        )
    
        

    except Exception as e:
        print("Error in prediction:", str(e))



# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
