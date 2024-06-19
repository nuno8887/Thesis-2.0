import main
import pprint

phrase = "TTabelaRegistos must have no more than 2 TTabelaSubRegistos and Camp is equal to 2 and Lamp is less than 4 and TTable is equal to 5."

docs, dic_main_CLOUSE, dic_if_CLOUSE, text = main.main(phrase)

# Print the updated dictionaries
print(text)
print()
print("dic_main_CLOUSE")
pprint.pprint(dic_main_CLOUSE)
print()
print("dic_if_CLOUSE")
pprint.pprint(dic_if_CLOUSE)
print()
print(docs)