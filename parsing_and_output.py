def parse(data: bytes) -> None:
    parsed_str = data[0:-2:1].decode('utf-8')
    output_to_screen(parsed_str)
    output_to_file(parsed_str)

def output_to_file(data: str) -> None:
    str = data.split(' ')
    with open('data.txt', 'a') as file:
        file.write(f'Спортсмен, нагрудный номер {str[0]}, '
                f'прошел отсечку {str[1]} в {str[2][:-2]}\n')

def output_to_screen(data: str) -> None:
    str = data.split(' ')
    if str[3] == '00':
        print(f'Спортсмен, нагрудный номер {str[0]}, '
            f'прошел отсечку {str[1]} в {str[2][:-2]}')