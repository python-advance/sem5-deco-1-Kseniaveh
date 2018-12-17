def get_valutes():
    import urllib.request
    from xml.etree import ElementTree #для работы с XML файлами
    
    resp = ElementTree.parse(urllib.request.urlopen("http://www.cbr.ru/scripts/XML_daily.asp")) #распарсиваем данные с сайта 
    valutes = {}
    #findall - находит только элементы с тегом, которые являются прямыми потомками текущего элемента
    for row in resp.findall('Valute'):
        valutes.update({row.find('CharCode').text: float(row.find('Value').text.replace(",", "."))})
    valutes.update({'RUB': 1})
    return valutes

"""Функций для постановки запятой в нужном месте"""
def print_valutes(valutes):
    result = ''
    i = 0
    for valute in valutes:
        if (i > 0):
            result += ',' + valute
        else:
            result += valute        
        i += 1
    print (result)


def write_log(func):
    import functools
    #функция обертка
    @functools.wraps(func)
    def wrapper(*args):
        result = func(*args)
        with open("logger.txt", "a") as f:
            f.write(("*" * 30) + "\n")
            f.write(args[3]+": " + str(args[2]) + "\n")
            f.write(args[4]+": " + str(result) + "\n")
            f.write(("*" * 30) + "\n")            
        return result
    return wrapper
    
@write_log
def calculate_valute(fromValuteValue,toValuteValue,unit,fromValute,toValute):
    koff = fromValuteValue / toValuteValue
    result = unit*koff
    return result

if __name__ == "__main__":
    valutes = get_valutes()
    print_valutes(valutes.keys())
    
        
    while True:
        try:
            fromValute = input("Выберите конвертируемую валюту: ")  
            toValute = input("Выберите конечную валюту: ") 
            
            fromValuteValue = valutes[fromValute]
            toValuteValue = valutes[toValute]
        except (KeyError):
            print("Таких валют не существует, убедитесь что вы правильно ввели")
            #созданы с целью того, чтобы программа не зацикливалась
            continue
        break
    
    while True:
        try:
            money = float(input("Введите количество единиц валюты: "))
        except (TypeError, ValueError):
            print("Вы ввели неправильное значение, нужно вводить число")
            continue
        break
    
    resultMoney = calculate_valute(fromValuteValue,toValuteValue, money,fromValute,toValute)
    
    print (fromValute+": "+str(money)+" = "+toValute+": "+str(resultMoney))
