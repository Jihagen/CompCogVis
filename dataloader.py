import os
from PIL import Image, ImageEnhance
import numpy as np
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
import torch
from torchvision.datasets import CIFAR10

class InfantVisionDataset(Dataset):
    def __init__(self, num_images=1000, data_source="photos", train=True, transformation_type="all", fixed_month=None):

        self.transform = transforms.ToTensor()
        self.transformation_type  = transformation_type
        self.fixed_month = fixed_month
        
        if data_source == "CIFAR":
            self.cifar10 = CIFAR10(root='./data', train=train, download=True, transform=None)
            self.num_images = min(num_images, len(self.cifar10))
            self.is_cifar = True
            self.labels = np.array([self.cifar10[i][1] for i in range(self.num_images)])

        else:
            self.image_paths = [os.path.join("photos", img) for img in os.listdir("photos") if img.endswith(('jpg', 'jpeg', 'png'))]
            self.num_images = min(num_images, len(self.image_paths))
            self.is_cifar = False
            self.labels = np.random.randint(0, 200, size=self.num_images)
        
        self.age_months = np.random.randint(0, 13, size=self.num_images) if fixed_month is None else [fixed_month] * self.num_images


    def __len__(self):
        return self.num_images

    def __getitem__(self, idx):
        if self.is_cifar:
            image, label = self.cifar10[idx]
        else:
            image_path = self.image_paths[idx]
            image = Image.open(image_path).convert('RGB')
            label = self.labels[idx]

        original_image = self.transform(image.copy()) 
        age = self.age_months[idx]

        if self.transformation_type == None:
            return original_image, original_image, label, age
    
        
        acuity_scale = self.get_acuity_scale(age)
        
        if self.transformation_type == "color":
            transformed_image = self.apply_color_transformation(image.copy(), age)
            transformed_image = self.transform(transformed_image)  
            return original_image, transformed_image, label, age
        
        if self.transformation_type == "acuity": 
            transformed_image = self.apply_acuity_scaling(image.copy(), acuity_scale)
            transformed_image = self.transform(transformed_image)  
            return original_image, transformed_image, label, age
        
        else: 
            transformed_image = self.apply_acuity_scaling(image.copy(), acuity_scale)
            transformed_image = self.apply_color_transformation(transformed_image, age)
            
        
        transformed_image = self.transform(transformed_image) 
        return original_image, transformed_image, label, age
    
    def get_acuity_scale(self, age_months):
        min_acuity = 20    
        max_acuity = 600
        max_age = 12
        acuity = max_acuity - (age_months / max_age) * (max_acuity - min_acuity)
        acuity = max(min_acuity, min(max_acuity, acuity))
        return acuity / 20

    def apply_acuity_scaling(self, image, scale):
        width, height = image.size
        new_size = (int(width / scale), int(height / scale))
        image = image.resize(new_size, Image.BILINEAR)
        image = image.resize((width, height), Image.BILINEAR)
        return image
    

    def apply_color_transformation(self, image, month):
    # Convert the image to an RGB array for channel manipulation
        image_array = np.array(image).astype(float)  # Convert to float for precise adjustments

        if month == 0:
            # Primarily grayscale with slight red enhancement
            red_channel = image_array[:, :, 0] * 0.15   # Enhance red
            green_channel = image_array[:, :, 1] * 0.15  # Suppress green
            blue_channel = image_array[:, :, 2] * 0.15   # Suppress blue
            image_array = np.stack([red_channel, green_channel, blue_channel], axis=2)
        
        elif month == 1:
            # Primarily grayscale with slight red enhancement
            red_channel = image_array[:, :, 0] * 0.255   # Enhance red
            green_channel = image_array[:, :, 1] * 0.15  # Suppress green
            blue_channel = image_array[:, :, 2] * 0.15  # Suppress blue
            image_array = np.stack([red_channel, green_channel, blue_channel], axis=2)
            
        elif month == 2:
            # Gradually introduce red and green
            red_channel = image_array[:, :, 0] * 0.35 # Visible red
            green_channel = image_array[:, :, 1] * 0.25 # Slight green visibility
            blue_channel = image_array[:, :, 2] * 0.1   # Blue remains suppressed
            image_array = np.stack([red_channel, green_channel, blue_channel], axis=2)

        elif month == 3:
            # Gradually introduce red and green
            red_channel = image_array[:, :, 0] * 0.4 # Visible red
            green_channel = image_array[:, :, 1] * 0.3 # Slight green visibility
            blue_channel = image_array[:, :, 2] * 0.1   # Blue remains suppressed
            image_array = np.stack([red_channel, green_channel, blue_channel], axis=2)

        elif month == 4:
            # Gradually introduce yellow, by matching red and green and suppressing blue
            red_channel = image_array[:, :, 0] * 0.4 # Visible red
            green_channel = image_array[:, :, 1] * 0.4 # Slight green visibility
            blue_channel = image_array[:, :, 2] * 0.15   # Blue remains suppressed
            image_array = np.stack([red_channel, green_channel, blue_channel], axis=2)

        elif month == 5:
            # Increase sensitivity to red, green, and yellow 
            red_channel = image_array[:, :, 0] * 0.5
            green_channel = image_array[:, :, 1] * 0.5
            blue_channel = image_array[:, :, 2] * 0.25  # Blue slightly more visible
            image_array = np.stack([red_channel, green_channel, blue_channel], axis=2)

        elif month == 6:
            # Increase sensitivity to red, green, and blue
            red_channel = image_array[:, :, 0] * 0.55
            green_channel = image_array[:, :, 1] * 0.55
            blue_channel = image_array[:, :, 2] * 0.3  # Blue slightly more visible
            image_array = np.stack([red_channel, green_channel, blue_channel], axis=2)
        
        elif month == 7:
            # Reduced saturation of full color
            red_channel = image_array[:, :, 0] * 0.65
            green_channel = image_array[:, :, 1] * 0.65
            blue_channel = image_array[:, :, 2] * 0.5
            image_array = np.stack([red_channel, green_channel, blue_channel], axis=2)

        elif month == 8:
            # Reduced saturation of full color
            red_channel = image_array[:, :, 0] * 0.75
            green_channel = image_array[:, :, 1] * 0.75
            blue_channel = image_array[:, :, 2] * 0.68
            image_array = np.stack([red_channel, green_channel, blue_channel], axis=2)
            
        elif month == 9:
            # Increase saturation to near-normal (80-90%)
            red_channel = image_array[:, :, 0] * 0.8
            green_channel = image_array[:, :, 1] * 0.8
            blue_channel = image_array[:, :, 2] * 0.77
            image_array = np.stack([red_channel, green_channel, blue_channel], axis=2)
        
        elif month == 10:
            # Increase saturation to near-normal (80-90%)
            red_channel = image_array[:, :, 0] * 0.88
            green_channel = image_array[:, :, 1] * 0.88
            blue_channel = image_array[:, :, 2] * 0.8
            image_array = np.stack([red_channel, green_channel, blue_channel], axis=2)
        
        elif month == 11:
            # Increase saturation to near-normal (80-90%)
            red_channel = image_array[:, :, 0] * 0.9
            green_channel = image_array[:, :, 1] * 0.9
            blue_channel = image_array[:, :, 2] * 0.9
            image_array = np.stack([red_channel, green_channel, blue_channel], axis=2)
        
        else:
            # Close to adult vision
            red_channel = image_array[:, :, 0] * 0.95
            green_channel = image_array[:, :, 1] * 0.95
            blue_channel = image_array[:, :, 2] * 0.95
            image_array = np.stack([red_channel, green_channel, blue_channel], axis=2)

        # Ensure values are within the valid range [0, 255]
        image_array = np.clip(image_array, 0, 255).astype(np.uint8)
        return Image.fromarray(image_array, 'RGB')
