import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns 
import json
import scipy.stats as stats
import re, os
import stanza

# stanza.download('en')

def count_images(x):
    return len(x)

def get_num(x):
    x = str(x)
    num = re.findall(r'[0-9]+', x)
    return int(num[0]) if num else -1

def check_num(x):
    return True if get_num(x) != -1 else False

nlp = stanza.Pipeline('en')

def check_fac(ner):
    fac = False
    for i in ner:
        if i.type == 'FAC':
            fac = True
            break

    return fac

def check_address(x):
    doc = nlp(x)
    return check_fac(doc.entities)

def get_address(x):
    doc = nlp(x)
    return doc.entities

def check_sqft(x):
    sq = re.findall(r'sq|sqft', x)
    return True if sq else False

def clean_type(x):
    xtype = x.strip().lower()
    if xtype != 'parking' and xtype != 'storage':
        xtype = 'parking'
    return xtype

def check_sqft(x):
    sq = re.findall(r'sq( )?$|sqft( )?$', x)
    return True if sq else False

def read_images(imnames, folder = 'sample-images'):
    img = plt.imread(f"{folder}/{imnames}") if folder else plt.imread(f"{imnames}")
    img = np.sum(img.reshape(-1, 3), axis = 0)
    return ','.join(list(map(str, img)))

def get_duplicates(df, cols):
    return df.duplicated(subset = cols, keep = False)

def outliers(feat):
    q1,q3 = np.quantile(feat, q = [.25, .75])
    iqr = q3 - q1
    t1, t2 = q1 - (1.5 * iqr), q3 + (1.5 * iqr)
    return t1, t2

def get_price_range(feats):
    t1, t2 = outliers(feats)
    new_feats = []
    for f in feats:
        if f == -1:
            new_feats.append('None')
        elif f <= t1:
            new_feats.append('low')
        elif (f > t1) and (f < t2):
            new_feats.append('normal')
        else:
            new_feats.append('high')
    return new_feats

def groupby_price_range(df):
    gdf = df.groupby('ad_location')['price']
    df['price_range'] = None
    for g in gdf:
        t_price = g[1]
        idx = t_price.index
        price_idx = idx[np.where(t_price > -1)[0]]
        ranges = get_price_range(t_price[price_idx])
        df.loc[price_idx, 'price_range'] = ranges

    return df['price_range']

def read_file(fname):
    with open(fname, 'r') as file:
        jfile = json.load(file)
        
    return jfile

def read_images(imnames, folder = None):
    try:
        x = np.random.choice([i for i in imnames if 'default_parking' not in i])
        img = plt.imread(f"{folder}/{x}") if folder else plt.imread(f"{x}")
        img = np.sum(img.reshape(-1, img.shape[-1]), axis = 0)
        return ','.join(list(map(str, img)))
    except Exception :
        return None

def read_images_from_db():
    file = read_file('info.json')['pages']
    df = pd.DataFrame(file)
    df['image_counts'] = df.images.apply(count_images)
    non_zero_ind = df[df.image_counts > 0].index
    print(non_zero_ind.shape)
    df['image_pxs'] = None
    df.loc[non_zero_ind, 'image_pxs'] = df.loc[non_zero_ind, 'images'].apply(lambda x : read_images(x, folder = None))

    return df.image_pxs

def get_duplicates(df, cols):
    return df.duplicated(subset = cols, keep = False)


def get_features(df): 
    
    validate = pd.DataFrame({})
    validate['id'] = df.id
    
    # image    
    validate['image_counts'] = df.images.apply(count_images)
    zero_ind = validate[validate.image_counts == 0].index
    non_zero_ind = validate[validate.image_counts > 0].index
    validate['has_image'] = True
    validate.loc[zero_ind, 'has_image'] = False
    
    # duplicate image
    df['image_pxs'] = None
    df.loc[non_zero_ind, 'image_pxs'] = df.loc[non_zero_ind, 'images'].apply(lambda x : read_images(x, folder = None))
    validate['has_duplicate_image'] = None
    validate.loc[non_zero_ind, 'has_duplicate_image'] = get_duplicates(df.loc[non_zero_ind], ['image_pxs'])
    
    # address     
    df['full_desc'] = df.name + ' ' + df.description
    validate['has_address'] = df.full_desc.apply(check_address)

    # hostname & ad_location
    df[['hostname', 'ad_location']] = df['hosted by'].str.split(', ', expand = True)
    validate[['hostname','ad_location']] = df['hosted by'].str.split(', ', expand = True)
    
    # amenities
    validate['amenities_counts'] = df['space details and features'].apply(count_images)
    
    # sqrt
    df['type of space'] = df['type of space'].apply(clean_type)
    sq_ind = df[df['type of space'] == 'storage'].index
    validate['has_sqft'] = None
    validate.loc[sq_ind, 'has_sqft'] = df.loc[sq_ind, 'full_desc'].apply(check_sqft)
    
    # space type
    validate['space_type'] = df['type of space']
    
    # duplicate ad
    validate['is_duplicate_ad'] = get_duplicates(df, ['name', 'price', 'description'])
    
    # tile and desc
    validate['has_title'] = df.name.apply(lambda x : True if len(x) > 0 else False)
    validate['has_description'] = df.description.apply(lambda x : True if len(x) > 0 else False)
    
    # price
    df.price = df.price.apply(get_num)
    validate['has_price'] = df.price.apply(check_num)
    validate['price_range'] = groupby_price_range(df)
    validate['price'] = df.price
    
    return validate


