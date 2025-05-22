
# Spatio-Temporal Air Quality Prediction using GNN

This project is a **Spatio-Temporal Graph Neural Network (GNN)** based system designed to predict air quality indicators (PM2.5 and PM10) from environmental data collected across various monitoring stations. It uses **PyTorch Geometric** for the model, **FastAPI** for the backend API, and **Vite** as the frontend framework.

## 🌐 Tech Stack

- **Backend**: FastAPI, PyTorch, PyTorch Geometric, Scikit-learn
- **Model**: Graph Attention Network (GAT) with temporal edge memory
- **Frontend**: Vite + React (assumed)
- **Data Handling**: Pandas, NumPy, CSV upload support
- **Deployment**: Uvicorn

## ⚙️ Features

- GAT-based model with temporal edge weight updates using GRU
- CSV-based air quality input via frontend
- Dynamic graph creation based on geographical and environmental similarity
- Scaled predictions returned as downloadable CSV

## 📁 Project Structure

```
.
├── model.py                      # SpatioTemporalGNN and TemporalEdgeWeightModule
├── graph_utils.py               # Graph creation logic from CSV
├── PredictionToSingleCSV.py     # Converts predictions to downloadable CSV
├── locations.py                 # Locations list used in CSV
├── scalers/
│   ├── x_scaler.pkl             # Scaler for node features
│   └── edge_attr_scaler.pkl    # Scaler for edge attributes
├── TemporalGNN.pth              # Trained model checkpoint
├── main.py                      # FastAPI app
├── frontend/                    # Vite frontend app (not included here)
└── README.md
```

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

> **Note**: Ensure you have PyTorch and `torch-geometric` installed with the appropriate CUDA version.

### 3. Install Frontend (Vite + React)

```bash
cd frontend
npm install
npm run dev
```

> Update `vite.config.js` or `.env` if needed to match the backend URL (`http://localhost:8000`).

### 4. Start the FastAPI Server

```bash
cd ..
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🔌 API Endpoints

### `/predict` (POST)
Predict air quality given node and edge features.

**Request body:**
```json
{
  "x": [[value1, value2, ..., valueN], ...],
  "edge_index": [[0, 1, ...], [1, 2, ...]],
  "edge_attr": [[w1], [w2], ...]
}
```

**Response:**
```json
[
  [pm2_5_value, pm10_value, ...],
  ...
]
```

### `/upload_csv/` (POST)
Upload a `.csv` file to generate graph, make prediction, and download results.

**CSV File Format Required:**
```csv
pm2_5,pm10,wind_speed,wind_direction,latitude,longitude,altitude
...
```

**Returns:** CSV file with predictions.

## 📄 Example `.csv` File

```csv
pm2_5,pm10,wind_speed,wind_direction,latitude,longitude,altitude
12,24,3.5,90,27.7172,85.3240,1350
15,30,2.8,75,27.6781,85.3206,1325
...
```

## 🧠 Model Details

- 2 GATConv layers with multi-head attention
- Temporal edge memory updated with GRU
- Inputs are normalized using `StandardScaler`
- Outputs are inverse transformed for readability

## 📬 Contribution

Feel free to fork the repo, open issues, or submit pull requests.

## 📜 License

This project is licensed under the MIT License.

## 🙋‍♂️ Author

Developed by a Computer Engineering student from IOE Pulchowk Campus.
