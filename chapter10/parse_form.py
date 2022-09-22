import requests


params = {'firstname': 'Ryan', 'lastname': 'Mitchell'}
r = requests.post('http://pythonscraping.com/pages/files/processing.php',
                  data=params)
r = requests.post('https://pythonscraping.com/pages/files/form.html', data=params)
print(r.text)
