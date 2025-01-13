import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os 

# Membaca dan membersihkan data
df_hour = pd.read_csv("D:\dicoding_DA_main_bike\Dashboard\hour.csv")
print(os.getcwd())
print(os.listdir("."))

# Membuat header
st.title("Data Analytic: Bike Sharing dataset")

# Menambahkan picture
with st.sidebar:
    st.image("D:\data-analisis-main_bike\data-analisis-main\dashboard\logo sepeda.png")

# Menambahkan sidebar
st.sidebar.title("Hasil Analisis")
st.sidebar.header("Pilih hasil analisis yang akan ditampilkan")

# Daftar pilihan analisis
analysis_option = st.sidebar.radio(
    'choose one',
    (
        'Trend Penyewaan Sepeda berdasarkan musim',
        'Trend Penyewaan Sepeda berdasarkan Cuaca',
        'Perbandingan Penyewaan Sepeda berdasarkan jenis penyewa',
        'Perbandingan Penyewaan Sepeda berdasarkan kategori hari',
        'Trend Penyewaan Sepeda per bulan'
    )
)

# Placeholder untuk menampilkan analisis yang dipilih
if analysis_option == 'Trend Penyewaan Sepeda berdasarkan musim':
    st.write("Visualisasi total pengguna sepeda berdasarkan musim")

    # Data hasil groupby
    df_grouped_season = df_hour.groupby(by='season').agg({
        'count': 'sum'
    }).reset_index()

    # Ambil data dari hasil groupby
    seasons = df_grouped_season['season']
    total = df_grouped_season['count']
    colors = ['orange','green','red','blue']

    # Buat figure dan axis menggunakan Streamlit
    fig, ax = plt.subplots(figsize=(6, 4))

    # Plot bar chart
    ax.bar(seasons, total, color=colors)

    # Tambahkan label dan judul
    ax.set_xlabel('Season')
    ax.set_ylabel('Total Penyewaan')
    ax.set_title('Trend Bike Rental by Season')

    # Format angka pada sumbu y
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

    # Tambahkan jumlah di atas bar
    for i, value in enumerate(total):
        ax.text(i, value + 5000, format(value, ','), ha='center', va='bottom', fontsize=10)

    # Tampilkan grafik di Streamlit
    st.pyplot(fig)

elif analysis_option == 'Trend Penyewaan Sepeda berdasarkan Cuaca':
    st.write("Visualisasi trend penyewaan sepeda berdasarkan Cuaca/Weather Situation")
    df_grouped = df_hour.groupby(by='weather_situation').agg({'count': 'sum'}).reset_index()
    weathersit = df_grouped['weather_situation']
    total = df_grouped['count']
    colors = ['orange','green','red','cyan']

    #buat fig dan plot bar chart
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(weathersit, total, color=colors)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    ax.set_xlabel('Weather Situation')
    ax.set_ylabel('Total Penyewaan')
    ax.set_title('Total Bike Rentals by Weather Situation')
    for i, value in enumerate(total):
        ax.text(i, value + 50000, format(value, ','), ha='center', va='bottom')
    plt.subplots_adjust(top=0.85, bottom=0.2, left=0.15, right=0.95, hspace=0.3, wspace=0.3)
    st.pyplot(fig)

elif analysis_option == 'Perbandingan Penyewaan Sepeda berdasarkan jenis penyewa':
    st.write("Visualisasi Grafik Penyewaan Sepeda berdasarkan user")

    # Hitung total keseluruhan dari 'casual' dan 'registered'
    total_casual = df_hour['casual'].sum()
    total_registered = df_hour['registered'].sum()
    
    # Data untuk bar chart
    tipe_penyewa = ['Casual', 'Registered']
    total_penyewaan = [total_casual, total_registered]

    # Membuat DataFrame dari data
    total_penyewa = pd.DataFrame({
        'Tipe Penyewa' : tipe_penyewa, 
        'Total Penyewaan': total_penyewaan
    })
        
    # Create a pie chart
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(total_penyewa['Total Penyewaan'], 
           labels=total_penyewa['Tipe Penyewa'], 
           autopct='%1.1f%%', 
           startangle=70, 
           colors=['#48D1CC', '#00FA9A'])
    ax.set_title('Total Bike Rentals by User Type')
    ax.axis('equal') 
    st.pyplot(fig)

elif analysis_option == 'Perbandingan Penyewaan Sepeda berdasarkan kategori hari':
    st.write("Visualisasi Grafik total rental bike berdasarkan kategori hari")

    # Kode untuk visualisasi pertanyaan pertama
    df_grouped = df_hour.groupby(by='category_days').agg({
        'casual': 'sum',
        'registered': 'sum'
    }).reset_index()

    #sesuaikan data menjadi long format
    df_melt = df_grouped.melt(id_vars='category_days', value_vars=['casual', 'registered'],
                              var_name='type', value_name='sum')
    # membuat figure dan plot
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x='category_days', y='sum', hue='type', data=df_melt, palette='Greens', ax=ax)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    ax.set_xlabel('Kategori Hari')
    ax.set_ylabel('Jumlah Penyewa')
    ax.set_title('Amount of Rental Bike by type user and category days')
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(format(height, ','),
                    (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='center',
                    xytext=(0, 5), textcoords='offset points')
    plt.subplots_adjust(top=0.85, bottom=0.2, left=0.15, right=0.95, hspace=0.3, wspace=0.3)
    st.pyplot(fig)

elif analysis_option == 'Trend Penyewaan Sepeda per bulan':
    st.write("Visualisasi grafik trend penyewaan sepeda per bulan")

    # Group data and calculate total rentals per month
    monthly_revenue = df_hour.groupby('month', observed=True)['count'].sum()

    # Ubah indeks bulan ke format yang sesuai (Jan, Feb, ...), agar urutan bulan sesuai
    monthly_revenue = pd.Series({
    'Jan': 134933,
    'Feb': 151352,
    'Mar': 228920,
    'Apr': 269094,
    'Mei': 331686,
    'Jun': 346342,
    'Jul': 344948,
    'Aug': 351194,
    'Sep': 345991,
    'Okt': 322352,
    'Nop': 254831,
    'Des': 211036
    })
    # Create a list of colors, initially all 'blue'
    colors = ['red' if month == 'Jan' else 'green'if month == 'Aug'
              else 'tab:blue' for month in monthly_revenue.index]

    # Buat figure dan axis menggunakan Streamlit
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot bar chart
    ax.bar(monthly_revenue.index, monthly_revenue.values, color=colors)

    # Menambahkan judul dan label
    ax.set_title('Month Revenue from Rental Bike', fontsize=14, pad=20)
    ax.set_xlabel('Bulan', fontsize=12, labelpad=10)
    ax.set_ylabel('Total Penyewaan', fontsize=12, labelpad=10)
    ax.tick_params(axis='x', rotation=45, labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(format(height, ','),
                    (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='center',
                    xytext=(0, 5), textcoords='offset points')
    plt.subplots_adjust(top=0.85, bottom=0.2, left=0.15, right=0.95, hspace=0.3, wspace=0.3)
    # Tampilkan grafik di Streamlit
    st.pyplot(fig)
