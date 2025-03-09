# model.py
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch_geometric
from torch_geometric.nn import GATConv

class TemporalEdgeWeightModule(nn.Module):
    def __init__(self, edge_dim, hidden_dim):
        super(TemporalEdgeWeightModule, self).__init__()
        self.gru = nn.GRU(edge_dim, hidden_dim)
        self.fc = nn.Linear(hidden_dim, edge_dim)

    def forward(self, edge_weights, edge_memory):
        edge_weights = edge_weights.unsqueeze(0)  # (1, num_edges, edge_dim)
        updated_memory, hidden = self.gru(edge_weights, edge_memory)
        updated_weights = self.fc(updated_memory).squeeze(0)  # (num_edges, edge_dim)
        return updated_weights, hidden
class SpatioTemporalGNN(nn.Module):
    def __init__(self, in_channels, hidden_dim, out_channels, edge_dim, dropout_rate=0.5, num_heads=4):
        super(SpatioTemporalGNN, self).__init__()
        self.edge_module = TemporalEdgeWeightModule(edge_dim, hidden_dim)
        
        # Adding multiple layers of GATConv
        self.gat1 = GATConv(in_channels, hidden_dim, edge_dim=edge_dim, heads=num_heads)
        self.gat2 = GATConv(hidden_dim * num_heads, hidden_dim, edge_dim=edge_dim, heads=num_heads)
        
        self.dropout = nn.Dropout(dropout_rate)  # Dropout layer
        self.fc_out = nn.Linear(hidden_dim * num_heads, out_channels)

    def forward(self, x, edge_index, edge_attr, edge_memory):
        updated_edge_attr, new_edge_memory = self.edge_module(edge_attr, edge_memory)
        
        # Multiple GAT layers
        x = self.gat1(x, edge_index, edge_attr=updated_edge_attr)
        x = F.relu(x)
        x = self.gat2(x, edge_index, edge_attr=updated_edge_attr)
        x = F.relu(x)
        
        x = self.dropout(x)  # Apply dropout
        x = self.fc_out(x)
        return x, updated_edge_attr, new_edge_memory
