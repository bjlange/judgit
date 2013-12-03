from pymongo import MongoClient
from bson.code import Code

# build a list of all of the words in post titles
# words will be lowercase

client = MongoClient()
db = client.reddit

print 'Building word list...'

# Use MongoDB's map reduce

# Split title into words
mapper = Code("""
function() {
    var splitter = /\W/g;
    var words = this.title.toLowerCase().split(splitter);
    emit(1, words);
}
""")

# Combine words into set using a JS object as a makeshift set
reducer = Code("""
function(key, word_lists) {
    var obj = {};
    for (var i = 0; i < word_lists.length; i++) {
        list = word_lists[i];
        for (var j = 0; j < list.length; j++) {
            obj[list[j]] = true;
        }
    }
    var bob = {
        words: Object.keys(obj)
    };
    return bob;
}
""")

results = db.posts.map_reduce(mapper, reducer, 'title_words')
for doc in results.find():
    print doc

word_list = []

print 'Done.'
