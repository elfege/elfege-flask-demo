class Story:
    """Madlib story"""
    
    def __init__(self, words, text):
        
        self.words = words
        self.text = text
        
     
    def create(inputs):  
        
        print(f"inputs: {inputs}")
        
        this_story = """Once upon a time in a long-ago {place}, 
        there lived a large {adjective} {noun}. 
        It loved to {verb} {plural-noun}."""
        
        for (key, val) in inputs.items():
            print(f"key = {key}")
            print(f"val = {val}")
            this_story = this_story.replace("{" + key + "}", val)         
        
        print(f"this_story: {this_story}")
        
               
        return this_story
         
         
    
    