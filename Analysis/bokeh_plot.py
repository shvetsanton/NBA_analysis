import numpy as np
import pandas as pd
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import CategoricalColorMapper, HoverTool, Slider, Select
from bokeh.layouts import row, column, widgetbox
from bokeh.io import curdoc

from scipy.stats import beta

# Read in the Datasets
df_players = pd.read_csv('../Data/Players.csv')
df_stats = pd.read_csv('/Users/ashvets/github/NBA_analysis/Data/Seasons_Stats.csv')


df_stats = df_stats[['Year', 'Player', 'Pos', 'Age', 'Tm', 'G', 'TS%', 'FG', 'FGA', 'FG%', '3P', '3PA', 
        '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'TRB', 'AST', 'STL', 'BLK', 
        'TOV', 'PTS']]
        
        
df_stats = df_stats.dropna()
df_stats.Year = df_stats.Year.astype(int)
df_stats['RB'] = df_stats['TRB']
del df_stats['TRB']

def fan_pts(pts, reb, ast, blk, st, to):
    "Returns a one statistic summary of a players performance"
    return (1*pts + 1.2*reb + 1.5*ast + 3*blk + 3*st - 1*to)
    
pd.options.display.float_format = '{:,.2f}'.format

df_stats['PTS_avg'] = df_stats['PTS'] / df_stats['G']
df_stats['AST_avg'] = df_stats['AST'] / df_stats['G']
df_stats['STL_avg'] = df_stats['STL'] / df_stats['G']
df_stats['RB_avg'] = df_stats['RB'] / df_stats['G']
df_stats['BLK_avg'] = df_stats['BLK'] / df_stats['G']
df_stats['TOV_avg'] = df_stats['TOV'] / df_stats['G']
df_stats['Fan_PTS'] = fan_pts(df_stats['PTS'], df_stats['RB'], df_stats['AST']
                              , df_stats['BLK'], df_stats['STL'], df_stats['TOV'])
df_stats['Fan_PTS_avg'] = df_stats['Fan_PTS'] / df_stats['G']
df_stats["3Pfract"] = df_stats["3PA"]/df_stats.FGA

def remove_duplicate_players(data_frame):
    """Removes duplicate rows of players which played for multiple teams during the season"""
    # Input should be just one season data
    
    player_occurrences = {}
    for i in range(len(data_frame)):
        player_name = data_frame.iloc[i]['Player']
        player_team = data_frame.iloc[i]['Tm']
        index_row = data_frame.index[i]
        if player_name not in player_occurrences:
            player_occurrences[player_name] = []
        player_occurrences[player_name].append((player_team, index_row))

    for key in player_occurrences:
        curr_list = player_occurrences[key]
        if len(curr_list) == 1:
            continue
        for team, index in curr_list:
            if team != "TOT":
                data_frame = data_frame.drop(index)
    return data_frame


def organize_data(season):
    df = pd.read_csv('Data/Seasons_Stats.csv') 
    df = df[df['Year'] == season]
    df = remove_duplicate_players(df)
    df = df[['Player', '3P', '3PA', '3P%', 'Tm', 'Year']]
    df = df[df['3PA'] > 20]
    a = beta.fit(list(df['3P%']),floc=0, fscale=1)[0]
    b =  beta.fit(list(df['3P%']),floc=0, fscale=1)[1]
    df['3PEstimate'] = (df['3P'] + a) / (df['3PA'] + a + b)
    df['a'] = df['3P'] + a
    df['b'] = df['3PA'] - df['3P'] + b
    print('alpha: ' + str(a))
    print('beta: ' + str(b))
    return (df, a, b)


palette = ['aliceblue','antiquewhite','aqua','aquamarine','azure','beige','bisque','black',
           'blanchedalmond','blue','blueviolet','brown','burlywood','cadetblue','chartreuse',
           'chocolate','coral','cornflowerblue','cornsilk','crimson','cyan','darkblue','darkcyan',
           'darkgoldenrod','darkgray','darkgreen','darkkhaki','darkmagenta','darkolivegreen',
           'darkorange','darkorchid','darkred','darksalmon','darkseagreen','darkslateblue',
           'darkslategray','darkturquoise','darkviolet','red']


# color_mapper = CategoricalColorMapper(factors=df_stats['Tm'].unique().tolist(),
#                                       palette=palette)

p1 = figure(x_axis_label='3 Point %', y_axis_label='Number of Players', tools='box_select')
p2 = figure(x_axis_label='3 Point %', y_axis_label='IDK', tools='box_select')

slider = Slider(title='Year', start=1980, end=2017, step=1, value=2017)
menu = Select(options=df_stats['Player'].unique().tolist(), value='J.J. Redick', title='Player')

# df, a, b = organize_data(slider.value)
x = np.linspace(0.01, 0.99, 100)
# y = beta.pdf(x, a, b)
# hist, edges = np.histogram(df['3P%'], normed=True, density=True, bins=30)
# df_top = df[df['Player'] == menu.value].iloc[0]
# y2 = beta.pdf(x, df_top['a'], df_top['b'])
# Year = slider.value
# new_player = menu.value

source = ColumnDataSource(data={'x_3p': df_stats['3PA'], 'y_3p': df_stats['3P'],
                                'Tm': df_stats['Tm'], 'x_2p': df_stats['2PA'],
                                'y_2p': df_stats['2P'], 'Year': df_stats['Year'],
                                'Player': df_stats['Player']})

                                
def callback(attr, old, new):
    
    df, a, b = organize_data(slider.value)
    
    new_x_3p = df_stats[(df_stats['Year'] == slider.value) &
                               (df_stats['Tm'] == menu.value)]['3PA']

    new_y_3p = df_stats[(df_stats['Year'] == slider.value) &
                               (df_stats['Tm'] == menu.value)]['3P']

    new_tm = df_stats[(df_stats['Year'] == slider.value) &
                             (df_stats['Tm'] == menu.value)]['Tm']

    new_x_2p = df_stats[(df_stats['Year'] == slider.value) &
                               (df_stats['Tm'] == menu.value)]['2PA']

    new_y_2p = df_stats[(df_stats['Year'] == slider.value) &
                               (df_stats['Tm'] == menu.value)]['2P']

    new_year = df_stats[(df_stats['Year'] == slider.value) &
                               (df_stats['Tm'] == menu.value)]['Year']

    new_player = df_stats[(df_stats['Year'] == slider.value) &
                                 (df_stats['Tm'] == menu.value)]['Player']

    source.data = {'x_3p': new_x_3p, 'y_3p': new_y_3p, 'Tm': new_tm, 'x_2p': new_x_2p,
                   'y_2p': new_y_2p, 'Year': new_year, 'Player': new_player}

    
#     source.data = {'hist': hist, 'edge_left': edges[:-1], 'edge_right': edges[1:], 'x': x, 'y': y, 'y2' : y2, 
#                    'Tm': new_tm, 'Year': new_year, 'Player': new_player}



    df, a, b = organize_data(slider.value)

    y = beta.pdf(x, a, b)    
    hist, edges = np.histogram(df['3P%'], normed=True, density=True, bins=30)
    edge_left = edges[:-1]
    edge_right = edges[1:]

    p1 = figure(title="Beta Approximation of 3P%", background_fill_color="#E8DDCB")
    p1.quad(top=hist, bottom=0, left=edge_left, right=edge_right, fill_color="#036564", line_color="#033649")
    p1.line(x, y, line_color="#D95B43", line_width=8, alpha=0.7, legend="Beta")
    p1.xaxis.axis_label = '3-Point Percentage'
    p1.yaxis.axis_label = 'Number of Players'
    p1.legend.location = "center_right"


    y2 = beta.pdf(x, df[df['Player'] == menu.value]['a'], df[df['Player'] == menu.value]['b'])

    p2 = figure(title="Bayesian Estimation", background_fill_color="#E8DDCB")
    p2.line(x, y, line_color="#D95B43", line_width=8, alpha=0.7, legend="Beta")
    p2.line(x, y2, line_color="#D95B43", line_width=8, alpha=0.7, legend="Player")
    
    column1 = column(widgetbox(menu), widgetbox(slider))
    layout = row(column1, p1, p2)

    curdoc().add_root(layout)
    
slider.on_change('value', callback)
menu.on_change('value', callback)

df, a, b = organize_data(slider.value)

y = beta.pdf(x, a, b)    
hist, edges = np.histogram(df['3P%'], normed=True, density=True, bins=30)
edge_left = edges[:-1]
edge_right = edges[1:]

p1 = figure(title="Beta Approximation of 3P%", background_fill_color="#E8DDCB")
p1.quad(top=hist, bottom=0, left=edge_left, right=edge_right, fill_color="#036564", line_color="#033649")
p1.line(x, y, line_color="#D95B43", line_width=8, alpha=0.7, legend="Beta")
p1.xaxis.axis_label = '3-Point Percentage'
p1.yaxis.axis_label = 'Number of Players'
p1.legend.location = "center_right"


y2 = beta.pdf(x, df[df['Player'] == menu.value]['a'], df[df['Player'] == menu.value]['b'])

p2 = figure(title="Bayesian Estimation", background_fill_color="#E8DDCB")
p2.line(x, y, line_color="#D95B43", line_width=8, alpha=0.7, legend="Beta")
p2.line(x, y2, line_color="#036564", line_width=8, alpha=0.7, legend=menu.value)

                   
                   
# p1.circle('x_3p', 'y_3p', source=source, alpha=0.8, nonselection_alpha=0.1,
#           color=dict(field='Tm', transform=color_mapper), legend='Tm')

# p2.circle('x_2p', 'y_2p', source=source, alpha=0.8, nonselection_alpha=0.1,
#           color=dict(field='Tm', transform=color_mapper), legend='Tm')

#p1.legend.location = 'bottom_right'
#p2.legend.location = 'bottom_right'


hover1 = HoverTool(tooltips=[('Player', '@Player')])
p1.add_tools(hover1)
hover2 = HoverTool(tooltips=[('Player', '@Player')])
p2.add_tools(hover2)

column1 = column(widgetbox(menu), widgetbox(slider))
layout = row(column1, p1, p2)

curdoc().add_root(layout)