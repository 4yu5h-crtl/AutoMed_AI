# ================================================
# 7. AGENT 4 — MODEL TRAINER (DYNAMIC)
# ================================================
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
import torchvision.transforms as T
from sklearn.metrics import f1_score
import os
from backend.logger import send_log


def build_model(selected_model, num_classes):
    if selected_model == "resnet":
        model = models.resnet18(pretrained=True)
        model.fc = nn.Linear(512, num_classes)

    elif selected_model == "efficientnet":
        model = models.efficientnet_b0(pretrained=True)
        model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)

    elif selected_model == "mobilenet":
        model = models.mobilenet_v2(pretrained=True)
        model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)

    else:
        raise ValueError("Invalid model selected")

    return model


def model_trainer_node(state):
    send_log("trainer", "Model Trainer Running...")

    dataset_path = state["dataset_path"]
    aug = state["aug_plan"]
    selected = state["selected_model"]["selected_model"]
    num_classes = len(state["dataset_stats"]["class_dist"])

    send_log("trainer", f"Selected Model: {selected}")
    send_log("trainer", f"Number of Classes: {num_classes}")

    # Build augmentation
    transform = T.Compose([
        T.Resize((224, 224)),
        T.RandomRotation(aug["rotation"]),
        T.RandomHorizontalFlip() if aug["flip"] else T.Lambda(lambda x: x),
    ])

    if aug["color_jitter"] == "low":
        transform.transforms.append(T.ColorJitter(brightness=0.1, contrast=0.1))
    elif aug["color_jitter"] == "medium":
        transform.transforms.append(T.ColorJitter(brightness=0.2, contrast=0.2))

    transform.transforms.append(T.ToTensor())

    # Load dataset
    train_dataset = ImageFolder(f"{dataset_path}/train", transform)
    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)

    # Build model
    model = build_model(selected, num_classes)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device)

    send_log("trainer", f"Training on: {device}")

    # Optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-4)

    all_preds, all_labels = [], []

    # QUICK training for demo
    for epoch in range(2):
        send_log("trainer", f"Epoch {epoch + 1}/2")

        for imgs, labels in train_loader:
            imgs = imgs.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            outputs = model(imgs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            preds = torch.argmax(outputs, dim=1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    # Metrics
    accuracy = sum(int(p == l) for p, l in zip(all_preds, all_labels)) / len(all_preds)
    f1 = f1_score(all_labels, all_preds, average="weighted")

    # Save model
    os.makedirs("models", exist_ok=True)
    model_path = f"models/{selected}_model.pt"
    torch.save(model.state_dict(), model_path)
    
    # Save class names
    import json
    classes_path = f"models/{selected}_classes.json"
    with open(classes_path, "w") as f:
        json.dump(train_dataset.classes, f)

    results = {
        "accuracy": float(accuracy),
        "f1_score": float(f1),
        "model": selected,
        "model_path": model_path
    }

    state["model_results"] = results

    send_log("trainer", "Training Complete. Results:")
    send_log("trainer", str(results))
    send_log("trainer", "Finished.")

    return state
