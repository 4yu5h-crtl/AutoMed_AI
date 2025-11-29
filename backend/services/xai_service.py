"""
Service layer for XAI (Explainable AI) functionality.
Generates Grad-CAM visualizations for model predictions.
"""
import torch
import torch.nn.functional as F
import cv2
import numpy as np
from torchvision import models, transforms
from PIL import Image
from typing import Tuple, Optional
import os


class GradCAM:
    """Grad-CAM implementation for CNN visualization."""
    
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        
        # Register hooks
        target_layer.register_forward_hook(self.save_activation)
        target_layer.register_backward_hook(self.save_gradient)
    
    def save_activation(self, module, input, output):
        self.activations = output.detach()
    
    def save_gradient(self, module, grad_input, grad_output):
        self.gradients = grad_output[0].detach()
    
    def generate(self, input_tensor, class_idx=None):
        """Generate Grad-CAM heatmap."""
        # Forward pass
        output = self.model(input_tensor)
        
        if class_idx is None:
            class_idx = output.argmax(dim=1).item()
        
        # Backward pass
        self.model.zero_grad()
        class_score = output[0, class_idx]
        class_score.backward()
        
        # Generate heatmap
        pooled_gradients = torch.mean(self.gradients, dim=[0, 2, 3])
        for i in range(self.activations.shape[1]):
            self.activations[:, i, :, :] *= pooled_gradients[i]
        
        heatmap = torch.mean(self.activations, dim=1).squeeze()
        heatmap = F.relu(heatmap)
        heatmap /= torch.max(heatmap)
        
        return heatmap.cpu().numpy(), class_idx, output[0, class_idx].item()


def load_model(model_name: str, model_path: str, num_classes: int = 2):
    """Load a trained model."""
    # Load weights first to determine num_classes
    state_dict = torch.load(model_path, map_location="cpu")
    
    # Infer number of classes from the last layer's weight shape
    if model_name == "resnet":
        # fc.weight shape is [num_classes, 512]
        num_classes = state_dict['fc.weight'].shape[0]
        model = models.resnet18(pretrained=False)
        model.fc = torch.nn.Linear(512, num_classes)
        target_layer = model.layer4[-1]
    elif model_name == "efficientnet":
        # classifier.1.weight shape is [num_classes, 1280]
        num_classes = state_dict['classifier.1.weight'].shape[0]
        model = models.efficientnet_b0(pretrained=False)
        model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, num_classes)
        target_layer = model.features[-1]
    elif model_name == "mobilenet":
        # classifier.1.weight shape is [num_classes, 1280]
        num_classes = state_dict['classifier.1.weight'].shape[0]
        model = models.mobilenet_v2(pretrained=False)
        model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, num_classes)
        target_layer = model.features[-1]
    else:
        raise ValueError(f"Unknown model: {model_name}")
    
    # Load weights
    model.load_state_dict(state_dict)
    model.eval()
    
    return model, target_layer


def generate_gradcam(
    image_path: str,
    model_name: str,
    model_path: str,
    num_classes: int = 2
) -> Tuple[np.ndarray, int, float, str]:
    """
    Generate Grad-CAM visualization for an image.
    
    Returns:
        heatmap_overlay: Image with heatmap overlay
        predicted_class: Predicted class index
        confidence: Prediction confidence
        explanation: Text explanation
    """
    # Load model
    model, target_layer = load_model(model_name, model_path, num_classes)
    
    # Load and preprocess image
    image = Image.open(image_path).convert("RGB")
    original_image = cv2.imread(image_path)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        # Note: Normalization removed to match training preprocessing
    ])
    
    input_tensor = transform(image).unsqueeze(0)
    
    # Generate Grad-CAM
    grad_cam = GradCAM(model, target_layer)
    heatmap, predicted_class, confidence = grad_cam.generate(input_tensor)
    
    # Resize heatmap to match image
    heatmap = cv2.resize(heatmap, (original_image.shape[1], original_image.shape[0]))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    
    # Overlay heatmap on original image
    overlay = cv2.addWeighted(original_image, 0.6, heatmap, 0.4, 0)
    
    # Try to load class names
    class_names = None
    try:
        import json
        classes_path = os.path.join(os.path.dirname(model_path), f"{model_name}_classes.json")
        if os.path.exists(classes_path):
            with open(classes_path, "r") as f:
                class_names = json.load(f)
    except:
        pass

    # Generate explanation
    explanation = generate_explanation(heatmap, predicted_class, confidence, class_names)
    
    return overlay, predicted_class, confidence, explanation


def generate_explanation(
    heatmap: np.ndarray, 
    predicted_class: int, 
    confidence: float,
    class_names: Optional[list] = None
) -> str:
    """Generate human-readable explanation of the prediction."""
    # Find regions of high activation
    gray_heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray_heatmap, 200, 255, cv2.THRESH_BINARY)
    
    # Calculate percentage of high activation
    activation_percentage = (np.sum(thresh > 0) / thresh.size) * 100
    
    class_label = f"Class {predicted_class}"
    if class_names and predicted_class < len(class_names):
        class_label = f"'{class_names[predicted_class]}'"
    
    if activation_percentage > 30:
        focus_area = "multiple distributed regions across the image"
        pattern_desc = "complex, widespread features"
    elif activation_percentage > 15:
        focus_area = "specific concentrated areas"
        pattern_desc = "distinctive structural patterns"
    else:
        focus_area = "highly localized features"
        pattern_desc = "fine-grained details"
    
    explanation = (
        f"The model has classified this image as {class_label} with a confidence score of {confidence*100:.1f}%. "
        f"The Grad-CAM analysis reveals that the model focused on {focus_area} to make this decision. "
        f"This suggests the model identified {pattern_desc} characteristic of {class_label} in these regions. "
        f"The heatmap overlay highlights these critical areas in red/yellow, indicating where the model's attention was strongest."
    )
    
    return explanation


def test_model_inference(
    image_path: str,
    model_name: str,
    model_path: str,
    num_classes: int = 2
) -> Tuple[int, float]:
    """
    Run inference on a single image.
    
    Returns:
        predicted_class: Predicted class index
        confidence: Prediction confidence
    """
    model, _ = load_model(model_name, model_path, num_classes)
    
    # Load and preprocess image
    image = Image.open(image_path).convert("RGB")
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        # Note: Normalization removed to match training preprocessing
    ])
    
    input_tensor = transform(image).unsqueeze(0)
    
    # Inference
    with torch.no_grad():
        output = model(input_tensor)
        probabilities = F.softmax(output, dim=1)
        confidence, predicted_class = torch.max(probabilities, dim=1)
    
    return predicted_class.item(), confidence.item()
