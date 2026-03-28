print("TEST BIBLIOTEK")
biblioteki =[
    "numpy",
    "scipy",
    "pandas",
    "matplotlib",
    "seaborn",
    "nibabel",
    "dipy",
    "sklearn",
    "statsmodels",
    "networkx",
    "bct",
    "brainspace",
    "neuromaps",
    "templateflow"
]
for lib in biblioteki:
    try:
        __import__(lib)
        print(f"{lib} - dziala")
    except Exception as e:
        print(f"{lib} - nie dziala: {e}")

print("Koniec testu")
