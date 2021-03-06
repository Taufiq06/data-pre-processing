import os
import pandas as pd
import urllib.request
from carto.datasets import DatasetManager
from carto.auth import APIKeyAuthClient
import boto3
from botocore.exceptions import NoCredentialsError
from zipfile import ZipFile

# name of table on Carto where you want to upload data
# this should be a table name that is not currently in use
dataset_name = 'ene_029a_energy_intensity' #check

# first, set the directory that you are working in with the path variable
# you can use an environmental variable, as we did, or directly enter the directory name as a string
# example: path = '/home/ene_029a_energy_intensity'
path = os.getenv('PROCESSING_DIR')+dataset_name
#move to this directory
os.chdir(path)

# create a new sub-directory within your specified dir called 'data'
data_dir = 'data/'
if not os.path.exists(data_dir):
    os.mkdir(data_dir)

'''
Download data and save to your data directory
'''
# insert the url used to download the data from the source website
url = 'http://databank.worldbank.org/data/download/SE4ALL_csv.zip' #check

# download the data from the source
raw_data_file = data_dir+os.path.basename(url)
raw_data_file_unzipped = raw_data_file.split('.')[0]
urllib.request.urlretrieve(url, raw_data_file)

#unzip source data
zip_ref = ZipFile(raw_data_file, 'r')
zip_ref.extractall(raw_data_file_unzipped)
zip_ref.close()

'''
Process data
'''
# read in csv file as Dataframe
df = pd.read_csv(raw_data_file_unzipped+'/SE4ALLData.csv')

# subset for renewable energy intensity data 
df_subset = df[df['Indicator Name'].str.contains('Energy intensity level of primary energy')]

#convert tables from wide form (each year is a column) to long form (a single column of years and a single column of values)
year_list = [str(year) for year in range(1990, 2017)] #check
df_long = pd.melt (df_subset, id_vars= ['Country Name' ,'Country Code'] ,
                                 value_vars = year_list,
                                 var_name = 'year',
                                 value_name = 'energy_intensity')

#convert year column from object to integer
df_long.year=df_long.year.astype('int64')

#save processed dataset to csv
csv_loc = data_dir+dataset_name+'_edit.csv'
df_long.to_csv(csv_loc, index=False)


'''
Upload processed data to Carto
'''
print('Uploading processed data to Carto.')
#set up carto authentication using local variables for username (CARTO_WRI_RW_USER) and API key (CARTO_WRI_RW_KEY)
auth_client = APIKeyAuthClient(api_key=os.getenv('CARTO_WRI_RW_KEY'), base_url="https://{user}.carto.com/".format(user=os.getenv('CARTO_WRI_RW_USER')))
#set up dataset manager with authentication
dataset_manager = DatasetManager(auth_client)
#upload dataset to carto
dataset = dataset_manager.create(csv_loc)
print('Carto table created: {}'.format(os.path.basename(csv_loc).split('.')[0]))
#set dataset privacy to 'Public with link'
dataset.privacy = 'LINK'
dataset.save()
print('Privacy set to public with link.')

'''
Upload original data and processed data to Amazon S3 storage
'''
def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=os.getenv('aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key'))
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        print("http://{}.s3.amazonaws.com/{}".format(bucket, s3_file))
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

print('Uploading original data to S3.')
# Copy the raw data into a zipped file to upload to S3
raw_data_dir = data_dir+dataset_name+'.zip'
with ZipFile(raw_data_dir,'w') as zip:
    zip.write(raw_data_file, os.path.basename(raw_data_file))

# Upload raw data file to S3
uploaded = upload_to_aws(raw_data_dir, 'wri-public-data', 'resourcewatch/'+os.path.basename(raw_data_dir))

print('Uploading processed data to S3.')
# Copy the processed data into a zipped file to upload to S3
processed_data_dir = data_dir+dataset_name+'_edit'+'.zip'
with ZipFile(processed_data_dir,'w') as zip:
    zip.write(csv_loc, os.path.basename(csv_loc))

# Upload processed data file to S3
uploaded = upload_to_aws(processed_data_dir, 'wri-public-data', 'resourcewatch/'+os.path.basename(processed_data_dir))
