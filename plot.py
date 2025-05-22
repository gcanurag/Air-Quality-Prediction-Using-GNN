import matplotlib.pyplot as plt

# Data from your log
epochs = [1, 2, 3]
train_loss = [0.0206, 0.0193, 0.0190]
val_loss = [0.0198, 0.0197, 0.0196]

# Plot
plt.figure(figsize=(6, 4))
plt.plot(epochs, train_loss, marker='o', label='Train Loss', color='blue')
plt.plot(epochs, val_loss, marker='s', label='Validation Loss', color='red')

# Labels and title
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Training vs Validation Loss')
plt.legend()
plt.grid(True)

# Show plot
plt.show()
