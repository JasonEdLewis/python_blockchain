## https://cmdlinetips.com/2018/01/5-examples-using-dict-comprehension/

## Dic Comprehension

# Takes a touple with its value pair and converts them into a dictionary (JS object)

> stats = [('age',32), ('weight',180),('height', 190)]
>
> > > dic_stats = {key:value for (key,value) in stats}
> > > dic_stats
> > > {'age': 32, 'weight': 180, 'height': 190}

## List Comprehension

# Pulls the values out of the dictionary and saves them into a list (JS array)

> > > dic = {'name':'jason', 'age':43, 'weight':175}
> > > values = [dic[key] for key in dic]
> > > values
> > > ['jason', 43, 175]

# This iteration just pulls the keys (without the values)

> > > keys = [key for key in dic]
> > > keys
> > > ['name', 'age', 'weight']

## To copy list use "range" selector `[:]`. This is equivalent to [0:-1] where the entire RANGE of elements are selected, essentially copying the whole list from the 1st to last item
# python_blockchain
