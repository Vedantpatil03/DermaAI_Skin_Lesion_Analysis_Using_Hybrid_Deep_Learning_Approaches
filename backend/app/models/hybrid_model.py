import torch
import torch.nn as nn
from torchvision import models


class HybridCNNViT(nn.Module):

    def __init__(self, num_classes=7):
        super().__init__()

        # ========================================
        # ResNet18 Branch
        # ========================================
        self.cnn = models.resnet18(weights=None)

        # Remove original ResNet18 classifier
        self.cnn.fc = nn.Identity()

        # ResNet18 output = 512 features

        # ========================================
        # ViT-B/16 Branch
        # ========================================
        self.vit = models.vit_b_16(weights=None)

        # Remove original ViT classifier
        self.vit.heads = nn.Identity()

        # ViT-B/16 output = 768 features

        # ========================================
        # Hybrid Classifier
        # ========================================
        self.classifier = nn.Sequential(

            # 512 + 768 = 1280
            nn.Linear(1280, 512),

            nn.ReLU(),

            nn.BatchNorm1d(512),

            nn.Dropout(),

            nn.Linear(512, 256),

            nn.ReLU(),

            nn.Dropout(),

            nn.Linear(256, num_classes)
        )

    def forward(self, x):

        # ResNet18 features
        cnn_features = self.cnn(x)

        # ViT features
        vit_features = self.vit(x)

        # Combine CNN + ViT
        combined_features = torch.cat(
            [cnn_features, vit_features],
            dim=1
        )

        # Classification
        output = self.classifier(
            combined_features
        )

        return output