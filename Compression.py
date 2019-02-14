#import the framework
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask import make_response
import pandas as pd
import json ,io, os
import requests
import argparse
import markdown as md
from werkzeug import secure_filename



#Create an instance of the Flask
app=Flask(__name__)
api =Api(app)



#-------------------------------------------------------------------------------
def findPref(m):
    "Given a list, returns the longest common leading component"
    if not m: return ''
    s1 = min(m)
    #print("s1",s1)
    s2 = max(m)
    #print(s2)
    for i, c in enumerate(s1):
       # print("i,c", (i,c))
        if c != s2[i]:
            return s1[:i]
    return s1




def encode(words):
    encodedData = []

    #print("_________________THE words are :", words)
    for i, word in enumerate(words):
        #print(i,word)
        if i != 0:  
          #print("here",word, words[i-1])
          prefixFound = findPref([word, words[i-1]])
          #encodedData.loc[i,"prefixCount"] =int(len(prefixFound))
          #encodedData.loc[i,"word"] = word[len(prefixFound):]
          #encodedData.loc[i,"prefixCountWord"] = str(len(prefixFound))+' ' + word[len(prefixFound):]
          encodedData.append(str(len(prefixFound))+' ' + word[len(prefixFound):])

        else:
          #base case
          #encodedData.loc[i,"prefixCount"] =0
          #encodedData.loc[i,"word"] = word
          #encodedData.loc[i,"prefixCountWord"] =  '0' +' '+word
          encodedData.append('0' +' '+word)
    
    #encodedData["prefixCountWord"] = encodedData["prefixCount"].astype(int)
    #print("ENCODED DATA", encodedData)
    return encodedData


def decode(words):
    decodedWords =[]
    for i in range(len(words)):
       current = words[i].split()
       if i != 0:

          prev = words[i-1].split()
          toAdd = prev[1]
          word  = toAdd[:int(current[0])] + current[1]
        
          decodedWords.append(word)
       if i == 0:
           decodedWords.append(current[1])

    return decodedWords
    
#--------------------------------------------------------------------------

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Page Not found'}), 404)

@app.errorhandler(405)
def not_found(error):
    return make_response(jsonify({'error': 'Method not allowed at requested URL'}), 415)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)	
	
@app.errorhandler(415)
def not_found(error):
    return make_response(jsonify({'error': 'Unsupported Media Type'}), 415)





@app.route("/")
def index():
  """present a readme.md file"""


  #Open Readme.md file
  with open(os.path.dirname(app.root_path)+"/README.md","r") as mdfile:

    content = mdfile.read()

    return md.markdown(content)





#-----------------------------------------------------
#            2 Classes defined below
#-----------------------------------------------------

class Compress(Resource):
    """ This class compresses the data requested by client """
    @app.route('/compress')
    def post (self):
        f = request.files['file']
        filename = secure_filename(f.filename) 
        with open(filename,"r") as file:
          words = file.read().split('\n')
        
        w = encode(words)
        #print("w",w)
        return w, 201

#Registering route with framework by declaring an explicit endpoint from the class Name
api.add_resource(Compress, "/compress")





class Decompress(Resource):
    """This class decompress the data requested by client"""

    def post (self):
        f = request.files['file']
        filename = secure_filename(f.filename) 
        #stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
        with open(filename,"r") as file:
          words = file.read().split('\n')
        
        w = decode(words)
        #print("w",w)
        return w, 201

# Registering route with framework by declaring an explicit endpoint from the class Name 
api.add_resource(Decompress, "/decompress")
    


#-----------------------------------------------------
#            Main
#-----------------------------------------------------

if __name__ == '__main__':
   app.run(debug =True)