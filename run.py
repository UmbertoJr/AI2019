from code import *


def run():
    names = [name_ for name_ in os.listdir("./problems") if "tsp" in name_]
    for name in names:
        filename = f"problems/{name}"
        instance = Instance(filename)
        instance.print_info()
        print(" ---  ")
        instance.plot_data()




if __name__ == '__main__':
    run()
