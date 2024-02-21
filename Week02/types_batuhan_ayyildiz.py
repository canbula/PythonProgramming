my_int=int(input("Please enter an integer : "))
my_float=float(input("Please enter a float : "))
my_bool=bool(int(input("""If you want your result to be true, type 1 or any number 
but if you want your result to be false, just type 0. : """)))  # pythonda true ifadeler sayı false ifadeler ise 0 bunu kullanmak istedim
my_complex=input("Please enter an complex number example 5+3j : ") # bu kısım biraz hataya açık ama örnekteki gibi yazarsak bir sorun olmayacak

complex_list=my_complex.split("+")   # split metodu ile + ile ayrılmış ifadeleri bir listeye attım
real_complex=float(complex_list[0])  # split ile listelediğim ifadeleri floata çevirdim
imagenery_complex=float(complex_list[1][0]) # burda j kısmını almadan string ifadenin sadece sayı kısmını alıp floata çevirdim
my_complex=complex(real_complex,imagenery_complex) # oluşturduğum real ve imagenery kıssımlarını kullanarak complex bir sayı ürettim

# f fonksiyonu ile değişkenlerimi yazdırdım

print(f"My integer number is {my_int}")
print(f"My float number is {my_float}")
print(f"My boolean expression is {my_bool}")
print(f"My complex expression is {my_complex}")


#yukarıda bu değerleri kullanıcıdan alsaydım nasıl yapardım diye düşünmek istedim aşağıda asıl istenen halleri var

my_int=8
my_float=8.7
my_bool=True
my_complex=95+7j





