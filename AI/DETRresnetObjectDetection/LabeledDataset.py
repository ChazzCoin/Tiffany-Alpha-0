from sklearn.model_selection import train_test_split
import pandas as pd
import glob

# Create a dictionary to store the image paths and labels
data = {'image_path':[], 'label':[]}

# Iterate through the images in each class directory
for label in ['class1', 'class2', 'class3']:
    for image_path in glob.glob(f'path/to/{label}/*.jpg'):
        data['image_path'].append(image_path)
        data['label'].append(label)

# Create a pandas dataframe from the dictionary
df = pd.DataFrame(data)

# Split the data into a training set and a validation set
train_df, val_df = train_test_split(df, test_size=0.2)

# Save the dataframe
train_df.to_csv("train_data.csv", index=False)
val_df.to_csv("val_data.csv", index=False)