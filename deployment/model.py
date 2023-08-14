import streamlit as st
from PIL import Image

def run():
    st.header('Stock Dataset')
    st.subheader('Model progress')
    penjelasan= 'Model Deep Neural Network yang di buat untuk forecast saham'
    st.write(penjelasan)
    st.markdown('---')

    st.write('#### Visualisation')
    class_names = ['Base','Improved']
    opsi = st.selectbox('choose model:', class_names)

    if opsi == 'Base':
        model_image = 'output_model_base.png'
        acc_image = 'output_mse_base.png'
        loss_image = 'output_loss_base.png'
        train_result = "Train RMSE: 1483.756"
        test_result = "Test RMSE: 1735.343"
    elif opsi == 'Improved':
        model_image = 'output_model_up.png'
        acc_image = 'output_mse_up.png'
        loss_image = 'output_loss_up.png'
        train_result = "Train RMSE: 160.766"
        test_result = "Test RMSE: 540.920"

    img1 = Image.open(model_image)
    img2 = Image.open(acc_image)
    img3 = Image.open(loss_image)
    st.image(img1, caption=f"picture of {opsi} model", use_column_width=True)
    st.image(img2, caption=f"picture of {opsi} accuracy", use_column_width=True)
    st.image(img3, caption=f"picture of {opsi} loss", use_column_width=True)
    st.write(train_result)
    st.write(test_result)

if __name__ == '__main__':
    run()
