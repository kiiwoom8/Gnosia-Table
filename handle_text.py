import data
import table_rendering

class HandleText:
    def __init__(self):
        self.text_lines = 0

    def print(self, text = ""):
        print(text)
        self.text_lines += 1

    def printr(self, text = ""):
        data.history.append(text)
        table_rendering.print_table()
        
    def input(self, text):
        result = input(text)
        self.text_lines += 1
        self.delete_text()
        return result
    
    def delete_text(self):
        for _ in range(self.text_lines):
            print("\033[F\033[K", end= "")
        self.text_lines = 0