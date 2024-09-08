class TextFormat:
    # Creates a formatted cell that can hold 38 characters
    @staticmethod
    def cell(substring) -> None:
        substring = str(substring)
        textfield = [" " for i in range(38)]

        substringLength = len(substring)
        textfield = textfield[:-substringLength]
    
        textfield.insert(3, substring)
        textfield.insert(0, "|")
        textfield.extend('|')
        

        return ''.join(textfield)
    
    # Creates a border out of '-' chars
    @staticmethod 
    def border():
        textfield = ["-" for i in range(38)]
        textfield.insert(0, "|")
        textfield.extend('|')

        return ''.join(textfield)

    
