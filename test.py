
def loadLayout(filepath):
        """We load the layout from the file"""
        f = open(filepath, 'r')
        for line in f:
            line = line.strip()
            print(line)
            for c in line:
                print(c)
                
                
            
    
def main():
    loadLayout("Game-Layout/layout")

if __name__ == '__main__':
    main()
