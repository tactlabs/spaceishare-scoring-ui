import numpy as np
import pandas as pd 


def get_score(dataframe):

    # dataframe.rename({'has_sqrt':'has_sqft'},axis=1,inplace=True)
    dataframe['has_sqft']=dataframe['has_sqft'].fillna('none')
    dataframe['price_range']=dataframe['price_range'].fillna('none')
    print('from scoring : ',dataframe.shape)
    ind=dataframe[dataframe.price_range == 'none'].index
    dataframe.loc[ind,'has_price']= False 

    l=[]
    for i in dataframe.index:
    # storing variables

        score = 0

        image_counts=dataframe.loc[i,'image_counts']
        has_address=dataframe.loc[i,'has_address']
        amenities_counts=dataframe.loc[i,'amenities_counts']
        has_price=dataframe.loc[i,'has_price']
        price_range=dataframe.loc[i,'price_range']
        has_sqft=dataframe.loc[i,'has_sqft']
        space_type=dataframe.loc[i,'space_type']
        has_image=dataframe.loc[i,'has_image']
        has_duplicate_image=dataframe.loc[i,'has_duplicate_image']
        is_duplicate_ad=dataframe.loc[i,'is_duplicate_ad']
        has_title=dataframe.loc[i,'has_title']
        has_description=dataframe.loc[i,'has_description']

        # image 25% weightage
        if image_counts>0:
            if has_duplicate_image:
                score += 5
            elif has_duplicate_image ==False:
                if image_counts>=2:
                    score += 25
                else:
                    score+=12.5
    
        #adress 15% weightage
        if has_address:
            score+=15
    
        #extra amenities 20% weightage
        
        if amenities_counts > 0:
            if amenities_counts>=4:
                score+=20
            else:
                score+= (amenities_counts * 5)
    
        # price range 10% weightage

        if has_price:
            if price_range=='low':
                score+=10
            elif price_range=='normal':
                score+=7.5
            elif price_range=='high':
                score+=5
    

        # title 5% weightage

        if has_title:
            score+=5

        # description 5% weightage

        if has_description:
            score+=5

        # dimensions 10% weightage
        
        print(has_sqft)
        if has_sqft:
            score+=10
        

        # not duplicate ad 10% weightage

        if not is_duplicate_ad:
            score+=10
        
        l.append(score)

    

    return l
    
    


    


            

