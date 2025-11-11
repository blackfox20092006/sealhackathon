import backend
with open('userstory-ex.txt', 'r', encoding='utf-8') as f:
    user_story = str([i.replace('\n', '') for i in f.readlines()])
with open('SRS-ex.txt', 'r', encoding='utf-8') as f:
    srs_data = str([i.replace('\n', '') for i in f.readlines()])
a = backend.SuggestionProcessor(user_story, srs_data)
A = a.process()
print(A)
b = backend.UserInteractionHandler('Please improve the SRS based on the suggestions.', A , srs_data)
B = b.process()
print(B)