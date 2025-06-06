import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import  keras.utils as utils
# from sklearn.preprocessing import LabelEncoder
# import matplotlib.pyplot as plt
import pandas as  pd
import io
model = tf.keras.models.load_model('model.h5')

arrKey = ["ayam", "daging_rendang", "dendeng_batokok", "gulai_ikan", "gulai_tambusu", "telur_balado",
          "telur_dadar", "tahu", "daun_singkong", "perkedel", "nasi", "tempe", "telur_mata_sapi",
          "mie", "udang"]

nutrition_facts = {
    "ayam": {"Protein (g)": 20, "Fat (g)": 10, "Carbohydrate (g)": 5, "Calories": 250},
    "daging_rendang": {"Protein (g)": 18, "Fat (g)": 15, "Carbohydrate (g)": 3, "Calories": 300},
    "dendeng_batokok": {"Protein (g)": 25, "Fat (g)": 12, "Carbohydrate (g)": 8, "Calories": 280},
    "gulai_ikan": {"Protein (g)": 22, "Fat (g)": 14, "Carbohydrate (g)": 6, "Calories": 270},
    "gulai_tambusu": {"Protein (g)": 19, "Fat (g)": 13, "Carbohydrate (g)": 7, "Calories": 280},
    "telur_balado": {"Protein (g)": 12, "Fat (g)": 9, "Carbohydrate (g)": 4, "Calories": 200},
    "telur_dadar": {"Protein (g)": 15, "Fat (g)": 11, "Carbohydrate (g)": 5, "Calories": 220},
    "tahu": {"Protein (g)": 10, "Fat (g)": 8, "Carbohydrate (g)": 3, "Calories": 180},
    "daun_singkong": {"Protein (g)": 5, "Fat (g)": 3, "Carbohydrate (g)": 2, "Calories": 100},
    "perkedel": {"Protein (g)": 8, "Fat (g)": 6, "Carbohydrate (g)": 4, "Calories": 150},
    "nasi": {"Protein (g)": 2, "Fat (g)": 1, "Carbohydrate (g)": 20, "Calories": 150},
    "tempe": {"Protein (g)": 15, "Fat (g)": 10, "Carbohydrate (g)": 5, "Calories": 250},
    "telur_mata_sapi": {"Protein (g)": 14, "Fat (g)": 9, "Carbohydrate (g)": 6, "Calories": 210},
    "mie": {"Protein (g)": 5, "Fat (g)": 3, "Carbohydrate (g)": 20, "Calories": 200},
    "udang": {"Protein (g)": 20, "Fat (g)": 10, "Carbohydrate (g)": 3, "Calories": 220}
}

def make_prediction(image_array):
    prediction = model.predict(image_array)
    prediction = arrKey[np.argmax(prediction)]
    return prediction

def load_image(uploaded_file):
    return io.BytesIO(uploaded_file.read())

def main():
    st.title('Fitter')
    uploadFile = st.file_uploader(label="upload image", type=['jpg', 'jpeg', 'png', 'webp'])
    st.sidebar.image("./fitter_logo.webp", width=150)
    st.sidebar.title("Hi! Welcome to Fitter ")
    st.sidebar.subheader("This is a Food Classification app that predicts the food class and provides nutrition facts.")
    st.sidebar.html('<p>We still still have limited amount of food that you can try to classify, this the the list</p>')
    st.sidebar.html('<lu><li>Rendang</li><li>Telur Matasapi</li><li>Ayam</li><li>Mie<li>Gulai Tambusu</li></lu>')
    if st.button('test prediction'):
        if uploadFile is not None:
            image = load_image(uploadFile)
            x = utils.load_img(image, target_size=(110, 110))
            x = utils.img_to_array(x)
            x = x.reshape(1, 110, 110, 3) / 255

            prediction = make_prediction(x)
            st.image(Image.open(image))
            st.write("Predicted Class:", prediction)
            
            confidence_score = np.max(model.predict(x))
            st.write("Confidence Score:", round(confidence_score, 4))

            if confidence_score < 0.85:
                st.warning("The model's prediction has a low confidence score (below 85%) and may not be reliable.")

            if prediction in nutrition_facts:
                st.subheader("Nutrition Facts:")
                nutrition_df = pd.DataFrame(nutrition_facts[prediction], index=[prediction])
                st.dataframe(nutrition_df)
            else:
                st.write("Nutrition facts not available for this predicted class.")
        else:
            st.error("Please upload an image before clicking the prediction button.")


if __name__ == '__main__':
    main()
