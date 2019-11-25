
import wikipedia
import wolframalpha
from tkinter import *
            
def res(event):
	ss=search.get("1.0",'end-1c')
	try:
		#wolframalpha
	    app_id = "L**************2"           #add your wolfarm id
	    client = wolframalpha.Client(app_id)
	    res = client.query(ss)
	    answer = next(res.results).text
	    #print (answer)
	    search.delete('1.0', END)
	    result.delete('1.0', END)
	    result.insert(END, answer)
	    
	except:
	    #wikipedia
	    #lang=self.txt.GetValue()
	    #wikipedia.set_lang(lang)
	    #print (wikipedia.summary(ss,sentences=5))
	    search.delete('1.0', END)
	    result.delete('1.0', END)
	    result.insert(END, wikipedia.summary(ss,sentences=5))


root=Tk()
root.title("Search Box")
Label(root,text="Search here.....").pack(side=TOP)

search=Text(root,height=1,width=50)
search.pack(side=TOP)

root.bind("<Return>",res)

Label(root,text="Search result.....").pack()

sy=Scrollbar(root)
sy.pack(side=RIGHT, fill=Y)

result=Text(root,height=5,width=100)
result.pack(side=LEFT, fill=Y)

sy.config(command=result.yview)
result.config(yscrollcommand=sy.set)

root.mainloop()
