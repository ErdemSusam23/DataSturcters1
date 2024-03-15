import pandas as pd

# Orijinal veri dosyasını okuyarak DataFrame'i oluştur
def read_original_data(filename):
    df = pd.read_csv(filename, header=None, names=["data"])
    return df

# DataFrame'i sırala ve yeni verileri ekleyerek güncelle
def update_sorted_data(original_data_df, new_data_filename):
    new_data_df = pd.read_csv(new_data_filename, header=None, names=["data"])
    combined_df = pd.concat([original_data_df, new_data_df], ignore_index=True)
    combined_df.sort_values(by="data", inplace=True)
    sorted_inserted_cumulative_sum(combined_df)
    return combined_df

# Belirtilen indeks numarasına sahip olan veriyi sil
def delete_by_index(data_df, index_filename):
    with open(index_filename, 'r') as file:
        indexes = file.readlines()
        indexes = [int(index.strip()) for index in indexes]
    data_df.drop(indexes, inplace=True)
    data_df.reset_index(drop=True, inplace=True)

# Yeni eklenmiş verilerin kümülatif toplamını hesapla ve yeni bir sütun olarak ekle
def sorted_inserted_cumulative_sum(data_df):
    data_df["cumulative_sum"] = data_df["data"].cumsum()

# Test etmek için kullanım
if __name__ == "__main__":
    original_data_filename = "C:\\Users\\livev\\OneDrive\\Masaüstü\\orginaldata.csv"
    delete_index_filename = "C:\\Users\\livev\\OneDrive\\Masaüstü\\deleteindex.csv"
    inserted_data_filename = "C:\\Users\\livev\\OneDrive\\Masaüstü\\inserteddata.csv"

    original_data_df = read_original_data(original_data_filename)
    updated_data_df = update_sorted_data(original_data_df, inserted_data_filename)
    delete_by_index(updated_data_df, delete_index_filename)

    print("Güncellenmiş DataFrame:")
    print(updated_data_df)
