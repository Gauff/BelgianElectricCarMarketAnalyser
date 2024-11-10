from collections import defaultdict, OrderedDict
import re

# Input list of makes and models
models = [
    'AIWAYS U5', 'AIXAM MEGA', 'AIXAM MYLI', 'AIXAM SCOUTY', 'AUDI E-TRON', 'AUDI E-TRON GT', 'AUDI E-TRON SPORTBACK',
    'AUDI Q4 E-TRON', 'AUDI Q4 SPORTBACK E-TRON', 'AUDI Q8 E-TRON', 'AUDI Q8 SPORTBACK E-TRON',
    'AUDI RS E-TRON', 'AUDI SQ8 E-TRON', 'AUSTIN MOKE', 'JIAYUAN CITY', 'BMW I3', 'BMW I4', 'BMW I5',
    'BMW I7', 'BMW IX', 'BMW IX1', 'BMW IX2', 'BMW IX3', 'BMW IX4', 'CITROEN AMI', 'CITROEN BERLINGO',
    'CITROEN C-ZERO', 'CITROEN DS3', 'CITROEN C4', 'CITROEN JUMPER', 'CITROEN JUMPY COMBI',
    'CITROEN SPACE TOURER', 'CUPRA BORN', 'DACIA SPRING', 'DS 3', 'FIAT 500', 'FIAT COUPE', 'FIAT DOBLO', 'FIAT SCUDO',
    'FISKER KARMA',
    'FISKER OCEAN', 'FORD TRANSIT', 'FORD MUSTANG', 'HONDA E', 'HONDA E:NY1', 'HYUNDAI IONIQ',
    'HYUNDAI IONIQ 5', 'HYUNDAI IONIQ 6', 'HYUNDAI KONA', 'JAC E-S2', 'JAGUAR I-PACE', 'JEEP AVENGER',
    'KIA E-NIRO', 'KIA SOUL', 'KIA EV6', 'KIA EV9', 'KIA NIRO', 'LEXUS RZ', 'LEXUS UX', 'LOTUS ELETRE',
    'MAZDA 2', 'MAZDA MX-30', 'MERCEDES EQ V', 'MERCEDES EQA', 'MERCEDES EQB', 'MERCEDES EQC',
    'MERCEDES EQE', 'MERCEDES EQE SUV', 'MERCEDES EQS', 'MERCEDES EQV', 'MERCEDES EQT', 'MERCEDES SPRINTER',
    'MERCEDES VITO', 'MERCEDES B ELECTRIC DRIVE', 'MG MARVEL R', 'MG MG4', 'MG MG5', 'MG ZS', 'MG 4', 'MG 5',
    'MINI COOPER',
    'MINI COUPE', 'MINI COUNTRYMAN', 'NISSAN ARIYA', 'NISSAN TOWNSTAR', 'NISSAN LEAF', 'NISSAN NV200',
    'MAXUS MIFA', 'MAXUS EDELIVER', 'MAXUS EUNIQ', 'MOVE VIGOROUS', 'OPEL AMPERA', 'OPEL COMBO',
    'OPEL CORSA', 'OPEL MOKKA', 'OPEL VIVARO', 'OPEL ZAFIRA', 'PACTA CARGO', 'PEUGEOT 2008', 'PEUGEOT 208',
    'PEUGEOT 3008', 'PEUGEOT 308',
    'PEUGEOT PARTNER', 'PEUGEOT ION', 'PEUGEOT RIFTER', 'PEUGEOT TRAVELLER', 'PEUGEOT EXPERT', 'PEUGEOT BOXER',
    'POLESTAR 2', 'PORSCHE TAYCAN',
    'RENAULT KANGOO', 'RENAULT MEGANE', 'RENAULT TWINGO', 'RENAULT TWIZY', 'RENAULT ZOE', 'SEAT MII',
    'SERES SERES 3', 'SKODA CITIGO', 'SKODA ENYAQ', 'SMART BRABUS', 'SMART FORFOUR', 'SMART FORTWO',
    'SMART FORTWO', 'SUBARU SOLTERRA', 'SSANGYONG KORANDO', 'TESLA MODEL 3', 'TESLA MODEL S',
    'TESLA MODEL X', 'TESLA MODEL Y', 'TESLA 3', 'TESLA S',
    'TESLA X', 'TESLA Y', 'TESLA ROADSTER', 'TESLA V2', 'TOYOTA AURIS', 'TOYOTA BZ4X', 'TOYOTA PROACE',
    'VOLKSWAGEN CRAFTER', 'VOLKSWAGEN GOLF', 'VOLKSWAGEN UP', 'VOLKSWAGEN ID.BUZZ', 'VOLKSWAGEN ID.3',
    'VOLKSWAGEN ID.4', 'VOLKSWAGEN ID.5', 'VOLVO C40', 'VOLVO EX30', 'VOLVO NH', 'VOLVO XC40',
    'STREETSCOOTER WORK', 'SUNRIDER SOLAR', 'RENAULT MASTER', 'MAN TGE', 'FIAT DUCATO'
]

grouped_models = {

}


def build_reference_list():

    car_dict = defaultdict(list)
    for model in models:
        make, model_name = model.upper().split(' ', 1)
        car_dict[make].append(model_name)
    # Sorting the values by their length in descending order
    for make in car_dict:
        car_dict[make] = sorted(car_dict[make], key=len, reverse=True)
    # Creating the second dictionary with cleaned model names
    reference_list = defaultdict(list)
    for make, model_list in car_dict.items():
        for model_name in model_list:
            cleaned_model_name = re.sub(r'[^A-Za-z0-9]', '', model_name.upper())  # Remove non-alphabetic characters
            reference_list[make.upper()].append([model_name, cleaned_model_name])
    sorted_cleaned_car_dict = OrderedDict(sorted(reference_list.items(), key=lambda item: -len(item[0])))
    # Converting defaultdict to regular dict for display
    #car_dict = dict(car_dict)
    reference_list = dict(sorted_cleaned_car_dict)
    # Print the result
    # print("Original dictionary:")
    # print(car_dict)
    # print("\nCleaned dictionary:")
    # print(reference_list)

    return reference_list


reference_list = build_reference_list()


def find_make_and_model(text):
    cleaned_text = (re.sub(r'[^A-Z0-9]', '', text.upper()))
    for make in reference_list.keys():
        if make in cleaned_text:
            for model_name, cleaned_model_name in reference_list[make]:
                if cleaned_model_name in cleaned_text:
                    return make, model_name
            return make, None
    return None, None


if __name__ == '__main__':
    ma, mod = find_make_and_model("skoda fabia")
    print(f"{ma} | {mod}")

# 'AIWAYS U5'
# 'AIXAM MEGA'
# 'AIXAM MYLI'
# 'AUDI E-TRON'
# 'AUDI E-TRON GT'
# 'AUDI E-TRON SPORTBACK'
# 'AUDI Q4 E-TRON'
# 'AUDI Q4 SPORTBACK E-TRON'
# 'AUDI Q8 E-TRON'
# 'AUDI Q8 SPORTBACK E-TRON'
# 'AUDI RS E-TRON'
# 'AUDI SQ8 E-TRON'
# 'AUSTIN MOKE'
# 'AUTRES JIAYUAN'
# 'BMW I3'
# 'BMW I4'
# 'BMW I5'
# 'BMW I7'
# 'BMW IX'
# 'BMW IX1'
# 'BMW IX2'
# 'BMW IX3'
# 'BMW IX4'
# 'CITROEN AMI'
# 'CITROEN BERLINGO'
# 'CITROEN C-ZERO'
# 'CITROEN DS3'
# 'CITROEN C4'
# 'CITROEN JUMPER'
# 'CITROEN JUMPY COMBI'
# 'CITROEN SPACE TOURER'
# 'CUPRA BORN'
# 'DACIA SPRING'
# 'DS 3'
# 'FIAT 500'
# 'FIAT COUPE'
# 'FISKER KARMA'
# 'FISKER OCEAN'
# 'FORD E-TRANSIT'
# 'FORD MUSTANG'
# 'HONDA E'
# 'HONDA E:NY1'
# 'HYUNDAI IONIQ'
# 'HYUNDAI IONIQ 5'
# 'HYUNDAI IONIQ 6'
# 'HYUNDAI KONA'
# 'JAC E-S2'
# 'JAGUAR I-PACE'
# 'JEEP AVENGER'
# 'KIA E-NIRO'
# 'KIA E-SOUL'
# 'KIA EV6'
# 'KIA EV9'
# 'KIA NIRO'
# 'LEXUS RZ'
# 'LEXUS UX'
# 'LOTUS ELETRE'
# 'MAZDA 2'
# 'MAZDA MX-30'
# 'MERCEDES EQ V'
# 'MERCEDES EQA'
# 'MERCEDES EQB'
# 'MERCEDES EQC'
# 'MERCEDES EQE'
# 'MERCEDES EQE SUV'
# 'MERCEDES EQS'
# 'MERCEDES EQV'
# 'MERCEDES EQT'
# 'MERCEDES SPRINTER'
# 'MERCEDES VITO'
# 'MERCEDES B ELECTRIC DRIVE'
# 'MG MARVEL R'
# 'MG MG4'
# 'MG MG5'
# 'MG ZS'
# 'MINI COOPER'
# 'MINI COUPE'
# 'MINI COUNTRYMAN'
# 'NISSAN ARIYA'
# 'NISSAN TOWNSTAR'
# 'NISSAN LEAF'
# 'NISSAN NV200'
# 'MAXUS MIFA'
# 'MAXUS EDELIVER'
# 'MAXUS EUNIQ'
# 'MOVE VIGOROUS'
# 'OPEL AMPERA'
# 'OPEL COMBO'
# 'OPEL CORSA'
# 'OPEL MOKKA'
# 'OPEL VIVARO'
# 'OPEL ZAFIRA'
# 'PACTA CARGO'
# 'PEUGEOT 2008'
# 'PEUGEOT 208'
# 'PEUGEOT PARTNER'
# 'PEUGEOT ION'
# 'PEUGEOT RIFTER'
# 'PEUGEOT TRAVELLER'
# 'POLESTAR 2'
# 'PORSCHE TAYCAN'
# 'RENAULT KANGOO'
# 'RENAULT MEGANE'
# 'RENAULT TWINGO'
# 'RENAULT TWIZY'
# 'RENAULT ZOE'
# 'SEAT MII'
# 'SERES SERES 3'
# 'SKODA CITIGO'
# 'SKODA ENYAQ'
# 'SMART BRABUS'
# 'SMART FORFOUR'
# 'SMART FORTWO'
# 'SMART FORTWO'
# 'SUBARU SOLTERRA'
# 'SSANGYONG KORANDO'
# 'TESLA MODEL 3'
# 'TESLA MODEL S'
# 'TESLA MODEL X'
# 'TESLA MODEL Y'
# 'TESLA ROADSTER'
# 'TOYOTA AURIS'
# 'TOYOTA BZ4X'
# 'TOYOTA PROACE'
# 'VOLKSWAGEN CRAFTER'
# 'VOLKSWAGEN GOLF'
# 'VOLKSWAGEN UP'
# 'VOLKSWAGEN ID.BUZZ'
# 'VOLKSWAGEN ID.3'
# 'VOLKSWAGEN ID.4'
# 'VOLKSWAGEN ID.5'
# 'VOLVO C40'
# 'VOLVO EX30'
# 'VOLVO NH'
# 'VOLVO XC40'
# 'STREETSCOOTER WORK'
# 'SUNRIDER SOLAR'
# 'RENAULT MASTER'
# 'MAN TGE'
# 'FIAT DUCATO'