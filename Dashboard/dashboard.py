import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime

# Membaca dan membersihkan data
df_hour = pd.read_csv("Dashboard/hour.csv")

# Membuat header
st.title("Data Analytic: Bike Sharing dataset")

# Menambahkan picture
with st.sidebar:
    st.image(Dashboard/logo sepeda.png")

# Tambahkan filter rentang tanggal di sidebar
st.sidebar.title("Filter Data")

date_range = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    value=(datetime.date(2011, 1, 1), datetime.date(2012, 12, 31)),  # Rentang default
    min_value=datetime.date(2011, 1, 1),
    max_value=datetime.date(2012, 12, 31)
)

# Pastikan pengguna memilih rentang tanggal (dua tanggal)
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    st.error("Harap pilih rentang tanggal (dua tanggal).")
    st.stop()

# Filter dataset berdasarkan rentang tanggal
df_hour['date'] = pd.to_datetime(df_hour['date'])  # Pastikan kolom tanggal dalam format datetime
df_filtered = df_hour[(df_hour['date'] >= pd.Timestamp(start_date)) & (df_hour['date'] <= pd.Timestamp(end_date))]
if df_filtered.empty:
    st.write("Tidak ada data untuk rentang tanggal yang dipilih. Silakan pilih rentang lain.")
    st.stop()

# Memilih hasil analisis
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
    df_grouped_season = df_filtered.groupby(by='season').agg({
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
    df_grouped = df_filtered.groupby(by='weather_situation').agg({'count': 'sum'}).reset_index()
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
        ax.text(i, value + 10000, format(value, ','), ha='center', va='bottom')
    plt.subplots_adjust(top=0.85, bottom=0.2, left=0.15, right=0.95, hspace=0.3, wspace=0.3)
    st.pyplot(fig)

elif analysis_option == 'Perbandingan Penyewaan Sepeda berdasarkan jenis penyewa':
    st.write("Visualisasi Grafik Penyewaan Sepeda berdasarkan user")

    # Hitung total keseluruhan dari 'casual' dan 'registered'
    total_casual = df_filtered['casual'].sum()
    total_registered = df_filtered['registered'].sum()
    
    # Data untuk bar chart
    tipe_penyewa = ['Casual', 'Registered']
    total_penyewaan = [total_casual, total_registered]

    # Membuat DataFrame dari data
    total_penyewa = pd.DataFrame({
    'Tipe Penyewa': ['Casual', 'Registered'],
    'Total Penyewaan': [df_filtered['casual'].sum(), df_filtered['registered'].sum()]
    })

    # Hapus baris dengan total penyewaan nol
    total_penyewa = total_penyewa[total_penyewa['Total Penyewaan'] > 0].dropna()

    # Jika semua nilai nol, tampilkan pesan error
    if total_penyewa.empty:
        st.write("Tidak ada data penyewaan sepeda untuk rentang tanggal yang dipilih.")
    else:

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
    df_grouped = df_filtered.groupby(by='category_days').agg({
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
    st.write(f"Visualisasi grafik trend penyewaan sepeda per bulan dari {start_date} hingga {end_date}")

    # Filter dataset berdasarkan rentang tanggal
    df_filtered['month'] = df_filtered['date'].dt.month  # Ekstrak bulan dari tanggal
    df_filtered['month_name'] = df_filtered['date'].dt.strftime('%b')  # Nama bulan (Jan, Feb, dll.)
    df_filtered['year'] = df_filtered['date'].dt.year  # Tambahkan tahun untuk membedakan tahun yang sama

    # Group data dan hitung total penyewaan per bulan
    monthly_revenue = df_filtered.groupby(['year', 'month', 'month_name'])['count'].sum().reset_index()

    # Urutkan data berdasarkan tahun dan bulan
    monthly_revenue = monthly_revenue.sort_values(by=['year', 'month'])

    # Plot visualisasi
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(
        x='month_name', y='count', hue='year', data=monthly_revenue,
        palette=['#32CD32', '#001C55'], ax=ax
    )

    # Tambahkan label dan judul
    ax.set_title('Monthly Bike Rentals (Filtered by Date)', fontsize=14, pad=20)
    ax.set_xlabel('Bulan', fontsize=12)
    ax.set_ylabel('Total Penyewaan', fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    ax.tick_params(axis='y', labelsize=10)

    # Tampilkan nilai pada bar
    for p in ax.patches:
        height = p.get_height()
        if height > 0:  # Tampilkan hanya jika nilai > 0
            ax.annotate(format(height, ','), 
                        (p.get_x() + p.get_width() / 2., height), 
                        ha='center', va='bottom', xytext=(0, 5), textcoords='offset points')

    # Tampilkan grafik di Streamlit
    st.pyplot(fig)
