def calculate_pyramid_height(b_num):
    a, b = 1, 0
    while b < b_num:
        b += a+1
        a += 1
        
        
    return a-1

if __name__ == "__main__":
    print(calculate_pyramid_height(15))