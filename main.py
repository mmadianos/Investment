from dataloader import DataLoader
from strategy import Strategy
from model import Model

ETFs = ['GLD', 'USO', 'CORN']
commodities = ['Gold', 'Oil', 'Corn']
map = dict(zip(commodities, ETFs))

strategy = Strategy(capital=10000, commodities=commodities)
data_train = DataLoader(ETFs, ['2009-1-1', '2013-12-31'])
data_test = DataLoader(ETFs, ['2014-1-1', '2017-12-31'])

list = data_train.data

models = {commodity: Model() for commodity in commodities}

for commodity, model in models.items():
    key = map[commodity]
    Y = data_train.data[key].pop('Close')
    model.train(data_train.data[key], Y)
