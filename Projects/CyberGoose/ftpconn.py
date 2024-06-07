from ftplib import FTP
from datetime import datetime

class FTPOperations:
    
    def __init__(self,host,port,username,password):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.ftp = FTP()
        self.ftp.connect(self.host,self.port)
        self.ftp.login(self.username, self.password)

    def open_folder(self,directory):
        dosya_listesi = []
        print("Directory: ")
        print(directory)
        self.ftp.cwd(directory)
        self.ftp.dir(dosya_listesi.append)
        j=0

        dosya_dict_listesi = []

        for line in dosya_listesi:
            # Satırları boşluklara göre bölelim
            j = j + 1
            parts = line.split()
            # Tarih ve dosya adını ayırarak alalım
            size = parts[4]
            date = ' '.join(parts[5:8])
            filename = ' '.join(parts[8:])
            # Yeni bir sözlük oluşturarak dosya adı ve zaman damgasını ekleyelim
            dosya_dict = {"Sira":j,"FileName": filename, "TimeStamp": date, "Size":str(size)+" Byte"}
            # Oluşturulan sözlüğü dosya_dict_listesi'ne ekleyelim
            dosya_dict_listesi.append(dosya_dict)

        return dosya_dict_listesi
    
    def dosya_yukle(self,sunucu_dosya_adi,dosyaadi):
        # Dosyayı sunucuya yükleme
        with open(dosyaadi, 'rb') as dosya:
            self.ftp.storbinary('STOR ' + sunucu_dosya_adi, open(dosyaadi, 'rb'))

    def dosya_indir(self, sunucu_dosya_adi, yerel_dosya_adi):
        with open(yerel_dosya_adi, 'wb') as dosya:
            self.ftp.retrbinary('RETR ' + sunucu_dosya_adi, dosya.write)

    def dosya_sil(self,dosyaadi):
        self.ftp.delete(dosyaadi)

    def get_file_details(self, filepath):
        details = {}
        try:
            # Dosya boyutunu al
            details['Size'] = self.ftp.size(filepath)
            
            # Dosyanın son değiştirilme tarihini al
            modify_time_str = self.ftp.sendcmd('MDTM ' + filepath)[4:].strip()
            modify_time = datetime.strptime(modify_time_str, "%Y%m%d%H%M%S")
            details['Change'] = modify_time.strftime('%Y-%m-%d %H:%M:%S')
            
            # Dosya izinlerini al
            response = []
            self.ftp.retrlines('LIST ' + filepath, response.append)
            details['filemod'] = self.rwx_to_octal(response[0].split()[0])
            
            # Dosya adı ve yolu
            details['FileName'] = filepath.split('/')[-1]
            details['FilePath'] = filepath
            details['Type'] = 'Directory' if response[0].startswith('d') else 'File'
            
            print("File details retrieved successfully!")
        except Exception as e:
            details['Error'] = str(e)
        return details

    def rwx_to_octal(self, rwx):
        """
        Sembolik dosya izinlerini (rwxrwxrwx) oktal formata çevirir (örn: '777').
        
        Args:
        rwx (str): Sembolik dosya izinleri (örn: 'rwxrwxrwx' veya 'rw-r--r--').
        
        Returns:
        str: Oktal formatta dosya izinleri (örn: '755').
        """
        permission_map = {'r': 4, 'w': 2, 'x': 1, '-': 0}
    
        user = sum(permission_map[char] for char in rwx[1:4])
        group = sum(permission_map[char] for char in rwx[4:7])
        other = sum(permission_map[char] for char in rwx[7:10])
    
        return f"{user}{group}{other}"
    
    def change_file_mode(self,dosyaadi,mod):
        self.ftp.sendcmd('SITE CHMOD ' + mod + ' ' + dosyaadi)
        print("Dosya izinleri başarıyla değiştirildi.")       
    
    
    def close(self):
        self.ftp.quit()
        print("Bağlantı kapatıldı")
#ftp = FTPOperations("192.168.0.6",21,"ftpusername","root")
#if __name__ == "__main__":
#    print(ftp.open_folder("/"))
# host ="ftpupload.net"
# port = 21
# username = "if0_36404009"
# password = "0920bilal"
