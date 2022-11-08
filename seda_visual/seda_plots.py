

import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

def fig_layout(template, fig, chart_titles=None, plots_colorscale='Plotly3',**kwargs):
    """
    Changing layout and styles
    :param template: Str, Plotly template
    :param fig: plotly.graph_objs._figure.Figure
    :param descr: Str
    :return: plotly.graph_objs._figure.Figure
    """
    if chart_titles == None:
        xaxis = (r'x (nm)')
        yaxis = (r'y (nm)')
        zaxis = (r'z (au)')
        title = (r'')
        chart_titles = {'x': xaxis, 'y': yaxis,'z':zaxis, 'title': title}
    
    fig.update_layout(showlegend=True,
                      template=template,
                      colorway=plots_colorscale,
                      paper_bgcolor='rgba(255,255,255,255)',
                      plot_bgcolor='rgba(255,255,255,255)',
                      width=900,
                      height=550,
                      xaxis=dict(
                          # title=f"{LABELS['RS']} [cm<sup>-1</sup>]",
                          title=f"{chart_titles['x']}",
                          linecolor="#777",  # Sets color of X-axis line
                          showgrid=False,  # Removes X-axis grid lines
                          linewidth=2.5,
                          showline=True,
                          showticklabels=True,
                          ticks='outside',
                      ),
    
                      yaxis=dict(
                          # title="Intensity [au]",
                          # title="Intensity [au]",
                          title=f"{chart_titles['y']}",
                          linecolor="#777",  # Sets color of Y-axis line
                          showgrid=True,  # Removes Y-axis grid lines
                          linewidth=2.5,
                      ),
                      title=go.layout.Title(text=chart_titles['title'],
                                            font=go.layout.title.Font(size=30)),

                      legend=go.layout.Legend(x=0.5, y=0 - .4, traceorder="normal",
                                              font=dict(
                                                  family="sans-serif",
                                                  size=14,
                                                  color="black",

                                              ),
                                              bgcolor="#fff",
                                              bordercolor="#ccc",
                                              borderwidth=0.4,
                                              orientation='h',
                                              xanchor='auto',
                                              itemclick='toggle',

                                              )),

    fig.update_yaxes(showgrid=True, gridwidth=1.4, gridcolor='#ccc')

    # plain hover
    fig.update_traces(hovertemplate=None)
    fig.update_layout(hovermode="x")
    return fig


# Adding traces, spectrum line design
def add_traces_single_spectra(df, fig, x, y, name):
    fig.add_traces(
        [go.Scatter(y=df.reset_index()[y],
                    x=df.reset_index()[x],
                    name=name,
                    line=dict(
                        width=3.5,  # Width of the spectrum line
                        color='#1c336d'  # color of the spectrum line
                        # color='#6C9BC0'  # color of the spectrum line
                    ),
                    )])
    return fig


def add_traces(df, fig, x, y, name, col=None):
    fig.add_traces(
        [go.Scatter(y=df.reset_index()[y],
                    x=df.reset_index()[x],
                    name=name,
                    line=dict(
                        width=3.5,
                    ),
                    )])
    return fig



def add_traces_3D(fig, data, name, col=None):
    nx = data.shape[0]
    ny = data.shape[1]
    xm,ym = np.meshgrid(np.arange(0, nx, 1), np.arange(0, ny, 1))
    x = np.arange(0, nx, 1)
    y = np.arange(0, ny, 1)
    fig.add_traces(
        [go.Scatter(y=df.reset_index()[y],
                    x=df.reset_index()[x],
                    name=name,
                    line=dict(
                        width=3.5,
                    ),
                    )])
    return fig


def fig_3d_2d_layout(data,template,pixel=5,**kwargs):
    z = data
    nx = data.shape[0]
    ny = data.shape[1]
    xm,ym = np.meshgrid(np.arange(0, nx, 1), np.arange(0, ny, 1))
    x = np.arange(0, nx, 1)
    y = np.arange(0, ny, 1)
    
    fig = make_subplots(
            rows=2, cols=2, 
            column_widths=[0.6, 0.4],
            row_heights=[0.6, 0.4],
            specs=[[{'type': 'surface','rowspan':2},{'type': 'contour'}],
                [None, {'type':'scatter'}]],
            horizontal_spacing=0.03,
            vertical_spacing=0.05,
            shared_xaxes=True,
            )
        # Generate data
    fig.add_trace(go.Surface(z=data.T, colorscale='Plotly3',showscale=False, reversescale=True),row=1, col=1)
    fig.add_trace(go.Heatmap(z=data.T, colorscale='Plotly3',reversescale=True,connectgaps=True, zsmooth='best'),row=1, col=2)
    fig.add_trace(go.Scatter(x=xm[0],y=data[:,pixel]),row=2,col=2)

    fig.update_layout(
        template=template,
            autosize=True,
            margin=dict(l=5, r=5, b=25, t=20),
        # width=1000,
        # height=500,
        font=dict(
            family="Latin Modern Roman,serif",
            color='white',
            size=13,
        ),   
            # xaxis2 = dict(title='x (nm)',tickvals=self.xt,ticktext=self.xtl)
        
    )
    return fig