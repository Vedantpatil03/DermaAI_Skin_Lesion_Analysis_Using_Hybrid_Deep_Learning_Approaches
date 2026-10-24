import torch
import torch.nn as nn


# ========================================
# DOUBLE CONVOLUTION BLOCK
# ========================================

class DoubleConv(nn.Module):

    def __init__(self, in_channels, out_channels):
        super().__init__()

        self.conv = nn.Sequential(
            nn.Conv2d(
                in_channels,
                out_channels,
                kernel_size=3,
                padding=1
            ),
            nn.ReLU(inplace=True),

            nn.Conv2d(
                out_channels,
                out_channels,
                kernel_size=3,
                padding=1
            ),
            nn.ReLU(inplace=True)
        )

    def forward(self, x):
        return self.conv(x)


# ========================================
# U-NET MODEL
# ========================================

class UNet(nn.Module):

    def __init__(self):

        super().__init__()

        # ========================================
        # ENCODER
        # ========================================

        self.down1 = DoubleConv(3, 64)
        self.pool1 = nn.MaxPool2d(2)

        self.down2 = DoubleConv(64, 128)
        self.pool2 = nn.MaxPool2d(2)

        self.down3 = DoubleConv(128, 256)
        self.pool3 = nn.MaxPool2d(2)

        self.down4 = DoubleConv(256, 512)
        self.pool4 = nn.MaxPool2d(2)

        # ========================================
        # BOTTLENECK
        # ========================================

        self.bottleneck = DoubleConv(
            512,
            1024
        )

        # ========================================
        # DECODER
        # ========================================

        self.up4 = nn.ConvTranspose2d(
            1024,
            512,
            2,
            2
        )

        self.conv4 = DoubleConv(
            1024,
            512
        )

        self.up3 = nn.ConvTranspose2d(
            512,
            256,
            2,
            2
        )

        self.conv3 = DoubleConv(
            512,
            256
        )

        self.up2 = nn.ConvTranspose2d(
            256,
            128,
            2,
            2
        )

        self.conv2 = DoubleConv(
            256,
            128
        )

        self.up1 = nn.ConvTranspose2d(
            128,
            64,
            2,
            2
        )

        self.conv1 = DoubleConv(
            128,
            64
        )

        # ========================================
        # OUTPUT
        # ========================================

        self.final = nn.Conv2d(
            64,
            1,
            kernel_size=1
        )

    def forward(self, x):

        # ========================================
        # ENCODER
        # ========================================

        c1 = self.down1(x)
        p1 = self.pool1(c1)

        c2 = self.down2(p1)
        p2 = self.pool2(c2)

        c3 = self.down3(p2)
        p3 = self.pool3(c3)

        c4 = self.down4(p3)
        p4 = self.pool4(c4)

        # ========================================
        # BOTTLENECK
        # ========================================

        bn = self.bottleneck(p4)

        # ========================================
        # DECODER
        # ========================================

        u4 = self.up4(bn)

        u4 = torch.cat(
            [u4, c4],
            dim=1
        )

        u4 = self.conv4(u4)

        u3 = self.up3(u4)

        u3 = torch.cat(
            [u3, c3],
            dim=1
        )

        u3 = self.conv3(u3)

        u2 = self.up2(u3)

        u2 = torch.cat(
            [u2, c2],
            dim=1
        )

        u2 = self.conv2(u2)

        u1 = self.up1(u2)

        u1 = torch.cat(
            [u1, c1],
            dim=1
        )

        u1 = self.conv1(u1)

        # ========================================
        # OUTPUT
        # ========================================

        return torch.sigmoid(
            self.final(u1)
        )